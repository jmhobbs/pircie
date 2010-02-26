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

import sys, os
from optparse import OptionParser
import ConfigParser

from twisted.internet import reactor

import pircie.plugins
import pircie.irc


def main ():

	# Add plugin libraries to lib
	sys.path.append( sys.path[0] + "/lib/" )

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

	plugins_config = config.get( 'Configuration', 'plugins' ).split( ',' )
	chain = []
	for pair in plugins_config:
		chain.append( pair.split( '|' ) )

	plugins = pircie.plugins.Plugins()
	plugins.load_plugins( sys.path[0] + "/plugins" )
	plugins.plugin_chain( chain )
	plugins.configure_plugins( bot_path, config )

	if 0 == len( plugins.plugins ):
		print "FATAL: No plugins loaded. Please check your configuration."
		exit()

	if options.dev_mode:
		print "-" * 10, "[ Loaded Plugins ]", "-" * 10
		for name,plugin in plugins.plugins.items():
			print name
		print "-" * 10, "[ Plugins Objects ]", "-" * 10
		for name,plugin in plugins.plugin_objects.items():
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