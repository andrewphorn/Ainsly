import plugins as plugin
from core import config

stfu = config.conf({}).setConfig('stfu').loadConfig()


@plugin.registerCommand('stfu',min_args=0,max_args=1,requires_op=True)
def stfuCommand(bot,user,channel,message):
	username = user.split('!')[0]
	if len(message) == 0:
		stfu.set(channel.lower(),not stfu.bool(channel.lower()))
		stfu.saveConfig()
	elif message[0].lower() in ['on','off']:
		stfu.set(channel.lower(),message[0].lower() == 'on')
		stfu.saveConfig()
	elif message[0].lower() == 'status':
		bot.sendNotice(username, 'I %s currently quiet' % ('am' if stfu.bool(channel.lower()) else 'am not'))

@plugin.registerEvent('SendMsgEvent',priority=0)
def stfuMsgEvent(bot,channel,message):
	return not stfu.bool(channel.lower())