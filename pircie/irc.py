# -*- coding: utf-8 -*-

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, task

class IRCBot ( irc.IRCClient ):

	plugins = None

	versionName = "pircie-bot"
	versionNum = "0.1"
	sourceURL = "http://github.com/jmhobbs/pircie"
	username = "%s-%s" % ( versionName, versionNum )
	nickname = None
	channel = None
	lineRate = 2

	def connectionMade ( self ):
		irc.IRCClient.connectionMade( self )
		print "Connection Made"

	def connectionLost( self, reason ):
		irc.IRCClient.connectionLost( self, reason )
		print "Connection Lost"

	def signedOn( self ):
		print "Signed On"
		self.join( self.channel )

	def joined( self, channel ):
		print "Joined:", channel
		self.channel = self.channel

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
			return

		print "Message:", user, msg, channel

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

		IRCBot.plugins = plugins
		IRCBot.channel = channel
		IRCBot.nickname = nickname

		# Now load our args
		if 'versionName' in kwargs:
			IRCBot.versionName = kwargs['versionName']
		if 'versionNum' in kwargs:
			IRCBot.versionNum = kwargs['versionNum']
		if 'sourceURL' in kwargs:
			IRCBot.sourceURL = kwargs['sourceURL']
		if 'username' in kwargs:
			IRCBot.username = kwargs['username']

	def clientConnectionFailed( self, connector, reason ):
		reactor.stop()