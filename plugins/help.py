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
		command = {'help':'Command not found.'}

	if command['help'] == 'None':
		command['help'] = '%s - No help available :(' % command['command']

	proto.sendMessage(channel,'%s: %s%s' % (user,proto.cmdprefix,command['help']))

