from twisted.internet import reactor,protocol
from core import protocol as proto

config = proto.config
AinslyProtocol = proto.AinslyProtocol

import plugins

proto.plugins = plugins

for plugin in config.list('plugins'):
	proto.plugins.load(plugin.lower())


factory = protocol.ReconnectingClientFactory()
factory.protocol = AinslyProtocol

reactor.connectTCP(config.string('server'),config.int('port'),factory)
print("Running AinslyBot")
reactor.run()