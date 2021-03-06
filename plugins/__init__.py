﻿from core.protocol import config, events, commands, log
import inspect, sys, traceback

handlers = {}

# Decorator to register an event handler.
def registerEvent(name,priority=5):
    def wrapper(func):
        plname = str(func.__module__).split('.',1)[1]
        log.debug("Registering event '%s' for plugin %s" % (name, plname))
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

# Decorator to register a command.
def registerCommand(name,requires_op=False,requires_voice=False,requires_admin=False,min_args=0, max_args=-1):
    def wrapper(func):
        log.debug("Registering command '%s'" % (name))
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

# Load a plugin
def load(plugin):
    """Loads a plugin by name"""
    plugin = plugin.lower()
    try:
        if ('plugins.%s' % plugin) in sys.modules:
            unload(plugin) # Make sure not to allow dupe events.
            reload(sys.modules['plugins.%s' % plugin])
        else:
            __import__("plugins.%s" % plugin)
    except ImportError,e:
        log.error('Failed to load plugin %s: %s' % (plugin,e))
    except Exception,e:
        log.error('Failed to load plugin %s - Helpful info')
        traceback.print_exc()
    return True

# Unload a plugin
def unload(plugin):
    """Unloads a plugin by name"""
    plugin = plugin.lower()
    try:
        if plugin in handlers:
            for evname in handlers[plugin]:
                for priority in handlers[plugin][evname]:
                    for func in handlers[plugin][evname][priority]:
                        if events.unregisterEvent(evname,func):
                            log.debug("Unregistered event: %s" % evname)
            del handlers[plugin]
    except Exception,e:
        log.error('Failed to unload plugin %s: %s' % (plugin,e))
    return True

@registerCommand('pll',requires_admin=True,min_args=1,max_args=1)
def commandLoadPlugin(proto, user, channel, args):
    """pll <plugin> - Loads <plugin>. Note that you can load plugins as many times as you want without adverse effects."""
    plugin = args[0].lower()
    if load(plugin):
        proto.sendMessage(channel, "Loaded %s" % plugin)
    else:
        proto.sendMessage(channel, "Failed to load %s - see console for details" % plugin)

@registerCommand('plu',requires_admin=True,min_args=1,max_args=1)
def commandUnloadPlugin(proto, user, channel, args):
    """plu <plugin> - Unloads <plugin>. Note that you can unload plugins as many times as you want without adverse effects."""
    plugin = args[0].lower()
    if unload(plugin):
        proto.sendMessage(channel, "Unloaded %s" % plugin)
    else:
        proto.sendMessage(channel, "Failed to unload %s - see console for details" % plugin)

@registerCommand('plr',requires_admin=True,min_args=1,max_args=1)
def commandReloadPlugin(proto,user,channel,args):
    """plr <plugin> - Reloads <plugin>. Similar to using the load command."""
    plugin = args[0].lower()
    if unload(plugin) and load(plugin):
        proto.sendMessage(channel, "Reloaded %s" % plugin)
    else:
        proto.sendMessage(channel, "Failed to reload %s - see console for details" % plugin)

