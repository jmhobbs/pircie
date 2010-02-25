# -*- coding: utf-8 -*-

import time

hooks = [ 'MESSAGE', 'WHISPER', 'JOINED', 'LEFT', 'NICK_CHANGE', 'ACTION' ]

def get_log_timestamp ():
	return time.strftime( "[%H:%M:%S]", time.localtime( time.time() ) )

def MESSAGE ( user, channel, message ):
	print "%s [%s] <%s> %s" % ( get_log_timestamp(), channel, user.split( '!' )[0], message )

def WHISPER ( user, message ):
	print "%s [WHISPER] <%s> %s" % ( get_log_timestamp(), user.split( '!' )[0], message )

def JOINED ( channel ):
	print "%s [JOINED] %s" % ( get_log_timestamp(), channel )

def LEFT ( channel ):
	print "%s [LEFT] %s" % ( get_log_timestamp(), channel )

def NICK_CHANGE ( old_nick, new_nick ):
	print "%s [NICK_CHANGE] <%s> is now known as <%s>" % ( get_log_timestamp(), old_nick, new_nick )

def ACTION ( user, channel, message ):
	print "%s [%s] * %s %s" % ( get_log_timestamp(), channel, user.split( '!' )[0], message )