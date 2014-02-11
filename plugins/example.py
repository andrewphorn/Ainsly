import plugins as plugin

@plugin.registerCommand('example')
def exampleCommand(bot,user,channel,message):
	bot.sendMessage(channel, '<%s> %s' % (user.split('!')[0], " ".join(message)))