# -*- coding: utf-8 -*-

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, task

class IRCBot ( irc.IRCClient ):

	versionName = None
	versionNum = None
	sourceURL = None
	username = None
	channel = None
	lineRate = 3

	instance = None

	def __init__ ( self ):
		self.versionName = self.factory.versionName
		self.versionNum = self.factory.versionNum
		self.sourceURL = self.factory.sourceURL
		self.username = self.factory.username
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

	def __init__( self, plugins, channel ):
		self.plugins = plugins
		self.channel = channel

	def clientConnectionFailed( self, connector, reason ):
		reactor.stop()