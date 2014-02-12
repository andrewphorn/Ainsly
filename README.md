Ainsly
======

A super simple ircbot framework that is designed to be super easy to make new plugins for.


Dependancies
------------

If you're on linux, I suggest getting most of these packages using pip or your package manager.

If you're on windows, most of these will be easier to get if you use pip or easy_instal.

**Note:** Twisted requires compilation, so if you're using windows, get the right installer.

|Package   |  Status      | Download      |
|----------|--------------|---------------|
|Twisted   |   Required   |  [Download](http://twistedmatrix.com/trac/wiki/Downloads)
|Zope.Interface | Required for twisted | [Download](http://pypi.python.org/pypi/zope.interface#download) (Suggestion: Use pip or easy_install) |
|PyOpenSSL |    Required for SSL  |  [Download](http://pypi.python.org/pypi/pyOpenSSL) (Windows users: Get the right installer!)|

Right now, Ainsly requires python 2.7, and it may or may not work on earlier versions. It does not currently work on Python 3.x, as Twisted has yet to be ported. Once Twisted is ported, Python3 compatibility will be added.


Documentation
-------------

#### Events

 * **SignedOn** - Called when signed on, but before joining channels.
    * Arguments: protocol

 * **NameListEnd** - Called when NameListend packet is found.
    * Arguments: protocol, channel

 * **MsgEvent** - Called when a privmsg is recieved
    * Arguments: protocol, user, channel, [message]

 * **SelfMsgEvent** - Called when a privmsg is being prepared to be sent
    * Arguments: protocol, channel, [message]

 * **NoticeEvent** - Called when a notice is recieved
    * Arguments: protocol, user, channel, [message]

 * **SelfKickEvent** - Called when your bot is kicked
    * Arguments: protocol, channel, kicker, [message]

 * **UserKickEvent** - Called when a kick event is recieved
    * Arguments: protocol, kickee, channel, kicker, [message]

 * **SelfJoinEvent** - Called when your bot joins a channel
    * Arguments: protocol, channel

 * **UserJoinEvent** - Called when your bot sees somebody join a channel
    * Arguments: protocol, user, channel

 * **SelfLeaveEvent** - Called when your bot leaves a channel
    * Arguments: protocol, channel

 * **UserLeaveEvent** - Called when your bot sees somebody leave a channel
    * Arguments: protocol, user, channel, [message]

 * **UserQuitEvent** - Called when your bot sees somebody leave the network
    * Arguments: protocol, user, [message]

 * **UserActionEvent** - Called when your bot sees somebody use an action (/me)
    * Arguments: protocol, user, channel, [message]

#### Examples

Here's a nice simple example plugin. You can find it in plugins/example.py.

```python
import plugins as plugin
from random import choice

@plugin.registerCommand('example')
def exampleCommand(bot,user,channel,message):
	bot.sendMessage(channel, '<%s> %s' % (user.split('!')[0], " ".join(message)))

@plugin.registerEvent('UserJoinEvent')
def exampleEvent(bot, user, channel):
	greetings = [
		'Hello, %s, I am a bot based on Ainsly! Learn more at https://github.com/andrewphorn/Ainsly',
		'Greetings, earthling named %s. You may call me... Frank.'
	]
	bot.sendMessage(channel, choice(greetings))
	bot.rc.callLater(2,exampleCallLater,bot,channel,"Oh yeah, almost forgot. I like pie!")

def exampleCallLater(bot,channel,message):
	bot.sendMessage(channel,message)
```

