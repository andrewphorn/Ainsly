# -*- coding: utf-8 -*-

import plugins as plugin


@plugin.registerCommand('help',min_args=0,max_args=1)
def helpCommand(proto,user,channel,words):
    """help [command] - Provides help for [command]. Displays this if no [command] is given."""
    user = user.split('!')[0]
    if len(words) == 0:
        command = proto.commands()['help']
    elif words[0].lower() in proto.commands().keys():
        command = proto.commands()[words[0].lower()]
    else:
        command = {'help':'%s - Command not found.' % words[0].lower()}

    if command['help'] == 'None':
        command['help'] = '%s - No help available.' % command['command']

    proto.sendNotice(user,'%s%s' % (proto.cmdprefix,command['help']))

@plugin.registerCommand('commands',min_args=0,max_args=0)
def commandsCommand(proto,user,channel,words):
    """commands - Provides a list of commands available to you in the channel where you called it."""
    cmdlist = []
    username = user.split('!')[0].lower()
    x=proto.commands()
    for cmd in x.keys():
        if x[cmd]['admin'] and proto.isAdmin(username):
            cmdlist.append(x[cmd]['command'].lower())
        elif x[cmd]['op'] and proto.isOP(username, channel.lower()):
            cmdlist.append(x[cmd]['command'].lower())
        elif x[cmd]['voice'] and proto.isVoice(username, channel.lower()):
            cmdlist.append(x[cmd]['command'].lower())
        elif True not in [x[cmd]['voice'],x[cmd]['op'],x[cmd]['admin']]:
            cmdlist.append(x[cmd]['command'].lower())

    cmds = ", ".join(cmdlist)
    proto.sendNotice(username, 'Available commands: %s' % cmds)
