# -*- coding: utf-8 -*-

import sys
import os

class Plugins:

	plugins = {}
	hooks = {}

	def __init__ ( self, path ):
		self.load_plugins( path )

	def load_plugins ( self, path ):
		sys.path.append( path )
		for root, dirs, files in os.walk( path ):
			for file in files:
				if file == 'plugin.py':
					import_path = root.replace( path, '' )[1:] + '/plugin'
					self.plugins[import_path] = __import__( import_path, None, None, [''] )
					for hook in self.plugins[import_path].hooks:
						if not self.hooks.has_key( hook ):
							self.hooks[hook] = []
						self.hooks[hook].append( import_path )

	def get_plugins_by_hook ( self, hook ):
		plugins = []
		if self.hooks.has_key( hook ):
			for plugin in self.hooks[hook]:
				plugins.append( self.plugins[plugin] )
		return plugins