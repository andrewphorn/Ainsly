import plugins as plugin
from core import config

nsdefault = {
    'enabled' : False,
    'nickserv': 'Nickserv',
    'account' : 'Ainsly',
    'password': 'Changeme'
}
ns_conf = config.conf(nsdefault).setConfig('nickserv').loadConfig()

havedone = {}

@plugin.registerEvent('NoticeEvent',priority=0)
def nickservMessage(bot,user,channel,message):
    if not ns_conf.bool('enabled'):
        return True

    if user.split('!')[0].lower() == ns_conf.string('nickserv').lower():
        if 'this nickname is registered' in " ".join(message).lower():
            bot.rc.callLater(.1,sendIdentifyString,bot)
        elif 'have identified' in " ".join(message).lower():
            if len(bot.channels) == 0 and havedone['forcejoin'] == True:
                print('now joining channels')
                bot.joinConfigChannels()
        else:
            print(" ".join(message).lower())

@plugin.registerEvent('SignedOn',priority=0)
def nickservPreventJoining(bot):
    if ns_conf.bool('enabled'):
        havedone['forcejoin'] = True
        bot.rc.callLater(2.5,joinAllChannels,bot)
        return False

@plugin.registerCommand('identify', requires_admin=True)
def timetoidentify(bot,user,channel,message):
    """identify - Identifies with nickserv if authentication is enabled"""
    if ns_conf.bool('enabled'):
        bot.rc.callLater(1,sendIdentifyString,bot)

def sendIdentifyString(bot):
    ident = ''
    if ns_conf.string('account') != '':
        ident = '%s ' % ns_conf.string('account')
    ident = 'IDENTIFY %s%s' % (ident,ns_conf.string('password'))
    bot.sendMessage(ns_conf.string('nickserv'), ident)
    print('Sent identify string')

def joinAllChannels(bot):
    if havedone['forcejoin'] == True:
        bot.joinConfigChannels()
        havedone['forcejoin'] = False
