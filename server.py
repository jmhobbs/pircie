# -*- coding: utf-8 -*-

import sys, os
from optparse import OptionParser
import ConfigParser

from twisted.internet import reactor

import pircie.plugins
import pircie.irc


def main ():

	parser = OptionParser( "usage: %prog [options] BOT_INI" )
	parser.add_option( "-d", "--dev", action="store_true", dest="dev_mode", default=False, help="run in dev mode" )
	(options, args) = parser.parse_args()

	if len( args ) == 0:
		print "FATAL: You must specify a bot configuration file to run.\n"
		parser.print_help()
		exit()

	bot_path = args[0].split( 'bot.ini' )[0]
	bot_ini = args[0]
	
	if not os.path.exists( bot_ini ):
		print "FATAL: Bot file does not exist: %s\n" % bot_ini
		parser.print_help()
		exit()
	
	config = ConfigParser.SafeConfigParser()
	config.read( bot_ini ) 

	active_plugins = config.get( 'Configuration', 'plugins' ).split( ',' )

	plugins = pircie.plugins.Plugins()
	plugins.load_plugins( sys.path[0] + "/plugins", active_plugins  )
	plugins.configure_plugins( bot_path, config )

	if 0 == len( plugins.plugins ):
		print "FATAL: No plugins loaded. Please check your configuration."
		exit()

	if options.dev_mode:
		print "-" * 10, "[ Loaded Plugins ]", "-" * 10
		for name,plugin in plugins.plugins.items():
			print name
		print "-" * 10, "[ Loaded Hooks ]", "-" * 10
		for hook,plgs in plugins.hooks.items():
			print hook
			for plugin in plgs:
				print " ", plugin
	else:
		factory = pircie.irc.IRCBotFactory( plugins, config.get( 'Configuration', 'channel' ), config.get( 'Configuration', 'nickname' ) )
		reactor.connectTCP( config.get( 'Configuration', 'server' ), config.getint( 'Configuration', 'port' ), factory )
		reactor.run()
	
if __name__ == "__main__":
	main()