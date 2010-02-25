# -*- coding: utf-8 -*-

import time

import os.path

hooks = [ 'MESSAGE', 'WHISPER', 'JOINED', 'LEFT', 'NICK_CHANGE', 'ACTION' ]

log_dir = None
log_date = None
log_handle = None

def init ( path, config ):

	if os.path.isabs( config.get( 'logger', 'directory' ) ):
		log_dir = config.get( 'logger', 'directory' )
	else:
		log_dir = path + config.get( 'logger', 'directory' )

	if not os.path.exists( log_dir ):
		print "ERROR: Logger could not find your log directory: %s" % log_dir
		return False

	log_date = time.strftime( "%Y-%m-%d", time.localtime( time.time() ) )

	try:
		log_handle = open( log_dir + log_date + ".log", 'a' )
	except IOError, e:
		print "ERROR: Logger could not open a file for writing in your log directory: %s" % log_dir
		return False

def log ( message ):
	#print log_date
	#global log_date
	#global log_handle
	#global log_dir

	#if log_date != time.strftime( "%Y-%m-%d", time.localtime( time.time() ) ):
		#log_handle.close()
		#log_date = time.strftime( "%Y-%m-%d", time.localtime( time.time() ) )
		#log_handle = open( log_dir + log_date + ".log", "a" )
		#log( '[log file rotation]' )
	#log_handle.write( '%s %s\n' % ( time.strftime( "[%H:%M:%S]", time.localtime( time.time() ) ), message ) )
	#log_handle.flush()

def MESSAGE ( bot, user, channel, message ):
	log( "[%s] <%s> %s" % ( channel, user.split( '!' )[0], message ) )

def WHISPER ( bot, user, message ):
	log( "[WHISPER] <%s> %s" % ( user.split( '!' )[0], message ) )

def JOINED ( bot, channel ):
	log( "[JOINED] %s" % ( channel ) )

def LEFT ( bot, channel ):
	log( "[LEFT] %s" % ( channel ) )

def NICK_CHANGE ( bot, old_nick, new_nick ):
	log( "[NICK_CHANGE] <%s> is now known as <%s>" % ( old_nick, new_nick ) )

def ACTION ( bot, user, channel, message ):
	log( "[%s] * %s %s" % ( channel, user.split( '!' )[0], message ) )