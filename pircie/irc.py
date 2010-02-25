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
		for plugin in self.plugins.get_plugins_by_hook( 'MADE_CONNECTION' ):
			plugin.MADE_CONNECTION()

	def connectionLost( self, reason ):
		irc.IRCClient.connectionLost( self, reason )
		for plugin in self.plugins.get_plugins_by_hook( 'LOST_CONNECTION' ):
			plugin.LOST_CONNECTION( reason )

	def signedOn( self ):
		for plugin in self.plugins.get_plugins_by_hook( 'SIGNED_ON' ):
			plugin.SIGNED_ON()
		self.join( self.channel )

	def joined( self, channel ):
		for plugin in self.plugins.get_plugins_by_hook( 'JOINED' ):
			plugin.JOINED( channel )

	def left( self, channel ):
		for plugin in self.plugins.get_plugins_by_hook( 'LEFT' ):
			plugin.LEFT( channel )

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
		if channel == self.nickname:
			for plugin in self.plugins.get_plugins_by_hook( 'WHISPER' ):
				plugin.WHISPER( user, msg )
		else:
			for plugin in self.plugins.get_plugins_by_hook( 'MESSAGE' ):
				plugin.MESSAGE( user, channel, msg )

	def action ( self, user, channel, msg ):
		for plugin in self.plugins.get_plugins_by_hook( 'ACTION' ):
				plugin.ACTION( user, channel, msg )

	def irc_NICK ( self, prefix, params ):
		old_nick = prefix.split('!')[0]
		new_nick = params[0]
		for plugin in self.plugins.get_plugins_by_hook( 'NICK_CHANGE' ):
			plugin.NICK_CHANGE( old_nick, new_nick )

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