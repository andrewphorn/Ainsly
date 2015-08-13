# -*- coding: utf-8 -*-
from twisted.internet import reactor, protocol
from twisted.words.protocols import irc

import events, config

import sys, os, time, re, traceback

config = config.confObject()
plugins = None
proto = None
commands = {}

MESSAGE_RE = re.compile(r'''((?:[^\s"']|"[^"]*"|'[^']*')+)''')

class AinslyProtocol(irc.IRCClient):
	"""Base protocol for the bot"""

	channels = {}
	data = {'users':{}}
	evqueue = {'msg':[],'ctcp':[],'notice':[],'ctcp':[]}
	nickname = config.string('nickname')
	realname = 'Ainsly v.2'
	ident = 'AinslyBot'
	cmdprefix = "" # Set the default cmd prefix in case we somehow get a message before config is loaded.
	rc = reactor # For convenience - you can still import twisted's reactor on your own.

	def commands(self):
		"""Lists commands. I am not good with computer."""
		global commands
		return commands

	def addCommand(self,cmd):
		"""Adds a command to the command list"""
		global commands
		commands[cmd['command'].lower()] = cmd

	def callEvent(self,name,*args):
		"""Calls an event, also passing the protocol along with it"""
		return events.callEvent(str(name),self,*args)

	def isAdmin(self,username):
		"""Checks for admin status in the bot"""
		return username.lower() == 'andrewph'

	def isOP(self,username,channel):
		"""Checks for OP status in a channel"""
		return username in self.channels.[channel.lower()]['users'] and (self.isAdmin(username) or self.channels[channel.lower()]['users'][username.lower()]['op'])

	def isVoice(self,username,channel):
		"""Checks for voice status in a channel"""
		return username in self.channels.[channel.lower()]['users'] and (self.isOP(username,channel) or self.channels[channel.lower()]['users'][username.lower()]['voice'])

	def irc_RPL_NAMREPLY(self, prefix, params):
		"""Called when a userlist is received for a channel"""
		channel = params[2].lower()
		if channel not in self.channels.keys():
			return

		self.channels[channel]['users'] = {}
		for user in params[3].split(' '):
			usr = user
			user = user.lower()
			u = {'op':False,'voice':False,'admin':False}
			if '@' in user:
				u['op'] = True
				user = user[1:]
				usr = usr[1:]
			if '+' in user:
				u['voice'] = True
				user = user[1:]
				usr = usr[1:]
			self.channels[channel]['users'][user] = u
			if user not in self.data['users']:
				self.data['users'][user] = {'nickname':str(usr),'admin':self.isAdmin(user)}

	def irc_RPL_ENDOFNAMES(self,prefix,params):
		"""Called when the userlist is completed for a channel"""
		channel = params[1].lower()

		self.callEvent('NameListEnd', channel)

	def signedOn(self):
		"""Called when the bot signs on"""
		reactor.callLater(.1,self.goThroughEvents)

		global proto
		self.cmdprefix = config.string('prefix')
		proto = self
		if self.callEvent('SignedOn'):
			self.joinConfigChannels()

	def joinConfigChannels(self):
		"""Joins the channels listed in the config"""
		for chan in config.list('channels'):
			chan = str(chan.lower())
			self.join(chan)

	def privmsg(self,user,channel,message):
		"""Called when the bot gets a message"""
		channel = channel.lower()
		username = user.split('!')[0].lower()
		print('<%s:%s> %s' % (user.split('!')[0],channel,message))
		if message.startswith(self.cmdprefix) and channel != self.nickname:
			# Filter out the prefix
			msg = message[len(self.cmdprefix):]

			# Command is going to be immediately after the prefix
			cmd = msg.split(' ')[0].lower()

			# Or not at all
			if cmd not in commands.keys():
				print("Is not in commands")
				print(cmd)
				return

			# Filter out the command from the args
			msg = msg[len(cmd):]

			# Smartfilter the string
			msg = MESSAGE_RE.split(msg)[1::2]

			# Get rid of pesky thingies
			for arg in msg:
				if arg.startswith("\"") and arg.endswith("\""):
					arg = arg[1:-1]
				elif arg.startswith("'") and arg.endswith("'"):
					arg = arg[1:-1]

			# if there's more than 0 messages, feed em in.
			if len(msg) > 0:
				args = msg
			else:
				args = []

			err = ''

			# is it a command?
			if cmd in commands.keys():
				# if it requires admin, is the user admin?
				if commands[cmd]['admin'] and not self.isAdmin(username):
					return

				# is it op or voice?
				if commands[cmd]['op'] or commands[cmd]['voice']:
					# is it voice?
					if commands[cmd]['voice'] and not self.isVoice(username,channel):
						return
					# is it op?
					elif commands[cmd]['op'] and not self.isOP(username, channel):
						return
				# does it have enough arguments?
				if len(args) < commands[cmd]['min_args']:
					err = 'Error: "%s" requires at least %s arguments' % (cmd,str(commands[cmd]['min_args']))
				# does it have too many arguments?
				if commands[cmd]['max_args'] > -1 and len(args) > commands[cmd]['max_args']:
					if err == '':
						err = 'Error: "%s" requires less than %s arguments' % (cmd, str(commands[cmd]['max_args']))
					else:
						err = '%s and less than %s arguments' % (err,str(commands[cmd]['max_args']))

				# is the error empty?
				if len(err) == 0:
					try:
						commands[cmd]['func'](self,user,channel,args)
					except Exception,e:
						self.sendMessage(channel,'An error occurred - Please check the bot console for more information.')
						traceback.print_exc()
				else:
					self.sendMessage(channel, err)
			return

		self.callEvent('MsgEvent', user, channel, message.split(' '))

	def noticed(self,user,channel,message):
		"""Called when the bot is noticed"""
		chan = channel.lower()
		message = message.split(' ')
		self.callEvent('NoticeEvent',user,chan,message)

	def userKicked(self, kickee, chan, kicker, message):
		"""Called when the bot or somebody else is kicked"""
		chan = chan.lower()
		username = kickee.split('!')[0]

		if username in self.channels[chan].keys():
			del self.channels[chan][username]

		if username == self.nickname:
			self.callEvent('SelfKickEvent', chan, kicker, message.split(' '))
			del self.channels[chan]
		else:
			self.callEvent('UserKickEvent', kickee, chan, kicker, message.split(' '))

	def joined(self,channel):
		"""Called when the bot joins."""
		channel = channel.lower()
		self.channels[channel] = {}
		self.callEvent('SelfJoinEvent', channel)

	def left(self,channel):
		"""Called when the bot leaves."""
		channel = channel.lower()
		del self.channels[channel]
		self.callEvent('SelfLeaveEvent', channel)

	def irc_NICK(self, old, new):
		"""Called when somebody other than the bot changes their nickname"""
		old = old.split('!')[0].lower()
		new = new[0].lower()
		new = new.lower()
		for chan in self.channels.keys():
			if old in self.channels[chan]['users']:
				self.channels[chan]['users'][new] = self.channels[chan]['users'].pop(old)

	def userJoined(self,user,channel):
		"""Called when somebody other than the bot joins."""
		chan = channel.lower()
		username = user.split('!')[0].lower()

		if username not in self.data['users']:
			self.data['users'][username] = {'nickname':str(user.split('!')[0]),'admin':self.isAdmin(user)}

		if username not in self.channels[chan]['users']:
			self.channels[chan]['users'][username] = {'op':False,'voice':False}

		self.callEvent('UserJoinEvent', user, channel)

	def userLeft(self,user,channel,reason=''):
		"""Called when somebody other than the bot leaves."""
		chan = channel.lower()
		username = user.lower()

		if username in self.data['users']:
			del self.data['users'][username]

		if username in self.channels[chan]['users']:
			del self.channels[chan]['users'][username]

		self.callEvent('UserLeaveEvent', user, channel, reason)

	def userQuit(self,user,message=''):
		"""Called when somebody other than the bot quits."""
		username = user.lower()
		if username in self.data['users']:
			del self.data['users'][username]

		for chan in self.channels.keys():
			if username in self.channels[chan]['users']:
				self.channels[chan]['users'][username]

		self.callEvent('UserQuitEvent', user, list(message.split(' ')))

	def modeChanged(self,user,channel,sign,modes,args):
		"""Called when a mode is changed in some channel"""
		i=-1
		for char in modes:
			i += 1
			if char in ['o','v']:
				if len(args) > i:
					if args[i].lower() in self.channels[channel.lower()]['users']:
						if char == 'o':
							self.channels[channel.lower()]['users'][args[i].lower()]['op'] = sign
						elif char == 'v':
							self.channels[channel.lower()]['users'][args[i].lower()]['voice'] = sign
		self.callEvent('ModeChangeEvent', user, channel, sign, modes, args)

	def action(self, user, channel, message):
		"""Called when somebody other than the bot uses an ACTION."""
		username = user.split('!')[0].lower()
		self.callEvent('UserActionEvent', user, channel, message)

	def unload_plugin(self,plugin):
		"""Protocol copy of plugins.unload"""
		plugins.unload(plugin)

	def load_plugin(self,plugin):
		"""Protocol copy of plugins.load"""
		plugins.load(plugin)

	def goThroughEvents(self):
		"""Loop through events (privmsgs, actions, ctcps, notices, etc) to prevent sending more than 1 of each at a time"""
		# messages
		if len(self.evqueue['msg']) > 0:
			m = self.evqueue['msg'].pop(0)
			if m[1].lower in ['q','nickserv']:
				self.msg(m[0],m[1])
			else:
				x = self.callEvent('SendMsgEvent', m[0], m[1])
				if x not in [True, None]:
					if x != False:
						self.msg(x[0],x[1])
				else:
					self.msg(m[0],m[1])

		# notices
		if len(self.evqueue['notice']) > 0:
			n = self.evqueue['notice'].pop(0)
			x = self.callEvent('SendNoticeEvent', n[0], n[1])
			if x not in [True, None]:
				if x != False:
					self.notice(x[0],x[1])
			else:
				self.notice(n[0],n[1])

		reactor.callLater(1,self.goThroughEvents)

	def sendMessage(self,target,words):
		"""Queue a message"""
		self.evqueue['msg'].append((target,words))

	def sendNotice(self,target,words):
		"""Queue a notice"""
		self.evqueue['notice'].append((target,words))


