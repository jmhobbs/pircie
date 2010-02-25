# -*- coding: utf-8 -*-

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, task

class IRCBot ( irc.IRCClient ):

	versionName = None
	versionNum = None
	sourceURL = None
	username = None
	nickname = None
	channel = None
	lineRate = 3

	def __init__ ( self ):
		self.versionName = self.factory.versionName
		self.versionNum = self.factory.versionNum
		self.sourceURL = self.factory.sourceURL
		self.username = self.factory.username
		self.nickname = self.factory.nickname
		self.lineRate = self.factory.lineRate

		irc.IRCClient.__init__( self )

	def connectionMade ( self ):
		irc.IRCClient.connectionMade( self )
		print "Connection Made"

	def connectionLost( self, reason ):
		irc.IRCClient.connectionLost( self, reason )
		print "Connection Lost"

	def signedOn( self ):
		print "Signed On"
		self.join( self.factory.channel )

	def joined( self, channel ):
		print "Joined:", channel
		self.channel = self.factory.channel

	def left( self, channel ):
		print "Left:", channel
		self.channel = None

	def try_say( self, msg ):
		"""
		Attempts to send the given message to the channel.
		"""
		if self.channel:
			try:
				self.say( self.channel, msg )
				return True
			except: pass

	def privmsg ( self, user, channel, msg ):
		user = user.split('!', 1)[0]

		if channel == self.nickname:
			print "Whisper:", user, msg

		if channel == self.channel:
			print "Message:", user, msg

	def action ( self, user, channel, msg ):
		print "Action:", user, channel, msg

	def irc_NICK ( self, prefix, params ):
		if self.logger:
			old_nick = prefix.split('!')[0]
			new_nick = params[0]
			print "Nick Swap:", old_nick, new_nick

class IRCBotFactory( protocol.ReconnectingClientFactory ):

	protocol = IRCBot

	def __init__( self, plugins, channel, nickname, **kwargs ):
		self.plugins = plugins
		self.channel = channel

		# Set defaults
		self.versionName = "pircie-bot"
		self.versionNum = "0.1"
		self.sourceURL = "http://github.com/jmhobbs/pircie"
		self.username = "%s-%s" % ( self.versionName, self.versionNum )
		self.nickname = nickname
		self.lineRate = 2

		# Now load our args
		if 'versionName' in kwargs:
			self.versionName = kwargs['versionName']
		if 'versionNum' in kwargs:
			self.versionNum = kwargs['versionNum']
		if 'sourceURL' in kwargs:
			self.sourceURL = kwargs['sourceURL']
		if 'username' in kwargs:
			self.username = kwargs['username']

	def clientConnectionFailed( self, connector, reason ):
		reactor.stop()