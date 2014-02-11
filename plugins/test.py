import plugins as plugin

@plugin.registerEvent('CmdEvent_test')
def TestCommand(proto,user,channel,args):
	"""/test <stuff>"""
	proto.msg(channel," ".join(args))
