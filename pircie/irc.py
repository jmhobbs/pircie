# -*- coding: utf-8 -*-

# Copyright (c) 2010 John Hobbs
#
# http://github.com/jmhobbs/pircie
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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

	def try_say( self, message, silent=False ):
		"""
		Attempts to send the given message to the channel.
		"""
		try:
			self.say( self.channel, message )
			if not silent:
				self.privmsg( self.nickname, self.channel, message )
			return True
		except:
			return False

	def connectionMade ( self ):
		irc.IRCClient.connectionMade( self )
		for plugin in self.plugins.get_plugins_by_hook( 'MADE_CONNECTION' ):
			if False == plugin.MADE_CONNECTION( self ):
				break

	def connectionLost( self, reason ):
		irc.IRCClient.connectionLost( self, reason )
		for plugin in self.plugins.get_plugins_by_hook( 'LOST_CONNECTION' ):
			if False == plugin.LOST_CONNECTION( self, reason ):
				break

	def signedOn( self ):
		for plugin in self.plugins.get_plugins_by_hook( 'SIGNED_ON' ):
			if False == plugin.SIGNED_ON( self):
				break
		self.join( self.channel )

	def joined( self, channel ):
		for plugin in self.plugins.get_plugins_by_hook( 'JOINED' ):
			if False == plugin.JOINED( self, channel ):
				break

	def left( self, channel ):
		for plugin in self.plugins.get_plugins_by_hook( 'LEFT' ):
			if False == plugin.LEFT( self, channel ):
				break

	def privmsg ( self, user, channel, msg ):
		if channel == self.nickname:
			for plugin in self.plugins.get_plugins_by_hook( 'WHISPER' ):
				if False == plugin.WHISPER( self, user, msg ):
					break
		else:
			first_word = msg.split( ' ' )[0]
			if first_word == self.nickname or first_word == self.nickname + ':' or first_word == '@' + self.nickname  or first_word == '@' + self.nickname + ':':
				for plugin in self.plugins.get_plugins_by_hook( 'ATME' ):
					atme_msg = " ".join( msg.split( ' ' )[1:] )
					if False == plugin.ATME( self, user, channel, atme_msg ):
						break
		
			for plugin in self.plugins.get_plugins_by_hook( 'MESSAGE' ):
				if False == plugin.MESSAGE( self, user, channel, msg ):
					break

	def action ( self, user, channel, msg ):
		for plugin in self.plugins.get_plugins_by_hook( 'ACTION' ):
			if False == plugin.ACTION( self, user, channel, msg ):
				break

	def irc_NICK ( self, prefix, params ):
		old_nick = prefix.split('!')[0]
		new_nick = params[0]
		for plugin in self.plugins.get_plugins_by_hook( 'NICK_CHANGE' ):
			if False == plugin.NICK_CHANGE( self, old_nick, new_nick ):
				break

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