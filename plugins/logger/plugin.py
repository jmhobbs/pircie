# -*- coding: utf-8 -*-

import time

from os.path import exists

hooks = [ 'MESSAGE', 'WHISPER', 'JOINED', 'LEFT', 'NICK_CHANGE', 'ACTION' ]

log_dir = None

def init ( path, config ):
	log_dir = path + config.get( 'logger', 'directory' )
	if not exists( log_dir ):
		print "[ERROR] Logger could not find your log directory: %s" % log_dir
		return False

def get_log_timestamp ():
	return time.strftime( "[%H:%M:%S]", time.localtime( time.time() ) )

def MESSAGE ( bot, user, channel, message ):
	print "%s [%s] <%s> %s" % ( get_log_timestamp(), channel, user.split( '!' )[0], message )

def WHISPER ( bot, user, message ):
	print "%s [WHISPER] <%s> %s" % ( get_log_timestamp(), user.split( '!' )[0], message )

def JOINED ( bot, channel ):
	print "%s [JOINED] %s" % ( get_log_timestamp(), channel )

def LEFT ( bot, channel ):
	print "%s [LEFT] %s" % ( get_log_timestamp(), channel )

def NICK_CHANGE ( bot, old_nick, new_nick ):
	print "%s [NICK_CHANGE] <%s> is now known as <%s>" % ( get_log_timestamp(), old_nick, new_nick )

def ACTION ( bot, user, channel, message ):
	print "%s [%s] * %s %s" % ( get_log_timestamp(), channel, user.split( '!' )[0], message )