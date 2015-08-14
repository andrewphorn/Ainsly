import os 
import sys
try:
    try:
        os.mkdir('data')
    except WindowsError:
        pass
except SyntaxError:
    # Linux
    pass
except Exception:
    print("Failed to create data directory, please create the directory yourself and re-run the bot.")
    sys.exit()

try:
    from twisted.internet import reactor,protocol
except ImportError:
    print("Failed to import Twisted, please install Twisted and Zope.interface")
    sys.exit()
from core import protocol as proto
from core import logger

import plugins

log = logger.LoggerClass()
proto.logger = log

config = proto.config
AinslyProtocol = proto.AinslyProtocol
proto.plugins = plugins

for plugin in config.list('plugins'):
    proto.plugins.load(plugin.lower())


factory = protocol.ReconnectingClientFactory()
factory.protocol = AinslyProtocol

reactor.connectTCP(config.string('server'),config.int('port'),factory)
log.log("Running AinslyBot")
reactor.run()