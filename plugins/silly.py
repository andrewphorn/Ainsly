# -*- coding: utf-8 -*-
import plugins as plugin

@plugin.registerCommand('donger', min_args=1, max_args=1)
def dongerCommand(proto,user,channel,words):
	user = user.split('!')[0]
	tf = False
	target = words[0].lower()
	for person in proto.channels[channel.lower()]['users']:
		if target in person.lower():
			target = person
			tf = True
	if tf:
		proto.sendMessage(channel, u'ヽ༼ຈل͜ຈ༽ﾉ %s has been dongered ヽ༼ຈل͜ຈ༽ﾉ if you do not donger 4 other people, you will be dongered to death ᕙ༼ຈل͜ຈ༽ᕗ raise ur dongers ヽ༼ຈل͜ຈ༽ﾉ'.encode('utf-8') % target)
