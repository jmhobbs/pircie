# -*- coding: utf-8 -*-

import sys

import pircie.plugins

p = pircie.plugins.Plugins( sys.path[0] + "/plugins" )

print p.get_plugins_by_hook( 'TEST' )
print p.get_plugins_by_hook( 'TESTB' )

