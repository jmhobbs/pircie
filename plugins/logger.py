# -*- coding: utf-8 -*-

import time

import os.path

class Plugin:

	hooks = [ 'MESSAGE', 'WHISPER', 'JOINED', 'LEFT', 'NICK_CHANGE', 'ACTION' ]

	log_dir = None
	log_date = None
	log_handle = None
	tty = False

	def configure ( self, path, config ):

		if os.path.isabs( config.get( 'logger', 'directory' ) ):
			self.log_dir = config.get( 'logger', 'directory' )
		else:
			self.log_dir = path + config.get( 'logger', 'directory' )

		if not os.path.exists( self.log_dir ):
			print "ERROR: Logger could not find your log directory: %s" % self.log_dir
			return False

		if 'True' == config.get( 'logger', 'tty' ):
			self.tty = True

		self.log_date = time.strftime( "%Y-%m-%d", time.localtime( time.time() ) )

		try:
			self.log_handle = open( self.log_dir + self.log_date + ".log", 'a' )
		except IOError, e:
			print "ERROR: Logger could not open a file for writing in your log directory: %s" % self.log_dir
			return False

	def log ( self, message ):
		if self.log_date != time.strftime( "%Y-%m-%d", time.localtime( time.time() ) ):
			self.log_handle.close()
			self.log_date = time.strftime( "%Y-%m-%d", time.localtime( time.time() ) )
			self.log_handle = open( self.log_dir + self.log_date + ".log", "a" )
			self.log( '[log file rotation]' )
		log_line = '%s %s\n' % ( time.strftime( "[%H:%M:%S]", time.localtime( time.time() ) ), message )
		self.log_handle.write( log_line )
		self.log_handle.flush()
		if self.tty:
			print log_line,

	def MESSAGE ( self, bot, user, channel, message ):
		self.log( "[%s] <%s> %s" % ( channel, user.split( '!' )[0], message ) )

	def WHISPER ( self, bot, user, message ):
		self.log( "[WHISPER] <%s> %s" % ( user.split( '!' )[0], message ) )

	def JOINED ( self, bot, channel ):
		self.log( "[JOINED] %s" % ( channel ) )

	def LEFT ( self, bot, channel ):
		self.log( "[LEFT] %s" % ( channel ) )

	def NICK_CHANGE ( self, bot, old_nick, new_nick ):
		self.log( "[NICK_CHANGE] <%s> is now known as <%s>" % ( old_nick, new_nick ) )

	def ACTION ( self, bot, user, channel, message ):
		self.log( "[%s] * %s %s" % ( channel, user.split( '!' )[0], message ) )