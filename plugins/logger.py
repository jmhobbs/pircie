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

import time

import os.path

class Plugin:

	hooks = [ 'MESSAGE', 'WHISPER', 'JOINED', 'LEFT', 'NICK_CHANGE', 'ACTION' ]

	log_dir = None
	log_date = None
	log_handle = None
	tty = False

	def configure ( self, path, config, name ):

		if os.path.isabs( config.get( name, 'directory' ) ):
			self.log_dir = config.get( name, 'directory' )
		else:
			self.log_dir = path + config.get( name, 'directory' )

		if not os.path.exists( self.log_dir ):
			print "ERROR: Logger could not find your log directory: %s" % self.log_dir
			return False

		if 'True' == config.get( name, 'tty' ):
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