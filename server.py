# -*- coding: utf-8 -*-

import sys, os
from optparse import OptionParser
import ConfigParser

from twisted.internet import reactor

import pircie.plugins
import pircie.irc


def main ():

	parser = OptionParser( "usage: %prog BOT_INI" )
	(options, args) = parser.parse_args()

	if len( args ) == 0:
		parser.error( "you must specify a bot configuration file to run." )

	bot_path = args[0].split( 'bot.ini' )[0]
	bot_ini = args[0]
	
	if not os.path.exists( bot_ini ):
		parser.error( "bot file does not exist: %s" % bot_path )
		return
	
	config = ConfigParser.SafeConfigParser()
	config.read( bot_ini ) 


	active_plugins = config.get( 'Configuration', 'plugins' ).split( ',' )
	plugins = pircie.plugins.Plugins()
	plugins.load_plugins( sys.path[0] + "/plugins", active_plugins  )

	factory = pircie.irc.IRCBotFactory( plugins, config.get( 'Configuration', 'channel' ), config.get( 'Configuration', 'nickname' ) )

	reactor.connectTCP( config.get( 'Configuration', 'server' ), config.getint( 'Configuration', 'port' ), factory )
	reactor.run()
	
if __name__ == "__main__":
	main()