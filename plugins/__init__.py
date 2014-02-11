from core.protocol import config, events, commands
import inspect, sys

handlers = {}

def registerEvent(name,priority=5):
	def wrapper(func):
		plname = str(func.__module__).split('.',1)[1]
		print("Registering event '%s' for plugin %s" % (name, plname))
		reg = events.registerEvent(str(name),func,int(priority))
		global handlers
		if plname not in handlers:
			handlers[plname] = {}

		if reg['name'] not in handlers[plname]:
			handlers[plname][reg['name']] = {}

		if reg['priority'] not in handlers[plname][reg['name']]:
			handlers[plname][reg['name']][reg['priority']] = []

		handlers[plname][reg['name']][reg['priority']].append(func)

	return wrapper

def registerCommand(name,requires_op=False,requires_voice=False,requires_admin=False,min_args=0, max_args=-1):
	def wrapper(func):
		print("Registering command '%s'" % (name))
		hlp = inspect.getdoc(func)
		cmd = {
			"command": str(name),
			"func": func,
			"help": str(hlp),
			"op": requires_op,
			"voice": requires_voice,
			"admin": requires_admin,
			"min_args": min_args,
			"max_args": max_args,
		}

		global commands
		commands[cmd['command']] = cmd
		
		return func
	return wrapper

def load(plugin):
	plugin = plugin.lower()
	try:
		if ('plugins.%s' % plugin) in sys.modules:
			reload(sys.modules['plugins.%s' % plugin])
		else:
			__import__("plugins.%s" % plugin)
		#for x in plu.eventHandlers:
		#	if len(x) < 3:
		#		x.append(5)
		#	events.registerEvent(x[0],x[1],x[2])
	except ImportError,e:
		print('Failed to load plugin %s: %s' % (plugin,e))
	return True

def unload(plugin):
	plugin = plugin.lower()
	try:
		if plugin in handlers:
			for evname in handlers[plugin]:
				for priority in handlers[plugin][evname]:
					for func in handlers[plugin][evname][priority]:
						if events.unregisterEvent(evname,func):
							print("Unregistered event: %s" % evname)
			del handlers[plugin]
		#for x in plu.eventHandlers:
		#	events.unregisterEvent(x[0],x[1])
	except Exception,e:
		print('Failed to unload plugin %s: %s' % (plugin,e))
	return True

@registerCommand('pll',requires_admin=True,min_args=1,max_args=1)
def commandLoadPlugin(proto, user, channel, args):
	"""pll <plugin> - Loads <plugin>"""
	plugin = args[0].lower()
	if load(plugin):
		proto.msg(channel, "Loaded %s" % plugin)
	else:
		proto.msg(channel, "Failed to load %s - see console for details" % plugin)

@registerCommand('plu',requires_admin=True,min_args=1,max_args=1)
def commandUnloadPlugin(proto, user, channel, args):
	"""plu <plugin> - Unloads <plugin>"""
	plugin = args[0].lower()
	if unload(plugin):
		proto.msg(channel, "Unloaded %s" % plugin)
	else:
		proto.msg(channel, "Failed to unload %s - see console for details" % plugin)

@registerCommand('plr',requires_admin=True,min_args=1,max_args=1)
def commandReloadPlugin(proto,user,channel,args):
	"""plr <plugin> - Reloads <plugin>"""
	plugin = args[0].lower()
	if unload(plugin) and load(plugin):
		proto.msg(channel, "Reloaded %s" % plugin)

