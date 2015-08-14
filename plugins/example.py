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
