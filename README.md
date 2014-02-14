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


#### Examples

Here's a nice simple example plugin. You can find it in plugins/example.py.

```python
import plugins as plugin
from random import choice

# Example of a command handler
@plugin.registerCommand('example')
def exampleCommand(bot,user,channel,message):
    bot.sendMessage(channel, '<%s> %s' % (user.split('!')[0], " ".join(message)))


# Example of an event handler
@plugin.registerEvent('UserJoinEvent')
def exampleEvent(bot, user, channel):
    greetings = [
        'Hello, %s, I am a bot based on Ainsly! Learn more at https://github.com/andrewphorn/Ainsly',
        'Greetings, earthling named %s. You may call me... Frank.'
    ]

    # Queue a message to be sent.
    ## Messages are sent once every half a second, to prevent spam.
    bot.sendMessage(channel, choice(greetings) % user.split('!')[0])

    # Call a function later, instead of doing it now.
    ## Take notes: we're calling exampleCallLater, and sending it 'bot', 'channel', and a message, in that order.
    bot.rc.callLater(2,exampleCallLater,bot,channel,"Oh yeah, almost forgot. I like pie!")

# This is gonna get called later, instead of instantly.
def exampleCallLater(bot,channel,message):
    bot.sendMessage(channel,message)
```

