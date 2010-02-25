# -*- coding: utf-8 -*-

import sys

from twisted.internet import reactor

import pircie.plugins
import pircie.irc

plugins = pircie.plugins.Plugins()
plugins.load_plugins( sys.path[0] + "/plugins" )

factory = pircie.irc.IRCBotFactory( plugins, 'pircie', 'pircie-bot' )

reactor.connectTCP( 'chat.freenode.net', 6667, factory )
reactor.run()