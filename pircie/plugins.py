# -*- coding: utf-8 -*-

import sys
import os

class Plugins:

	plugins = {}
	hooks = {}

	def load_plugins ( self, path, restrict=None ):
		"""
		Load all the plugins on a given path.
		
		path - A system path
		restrict - A collection of plugin names you want to be limited to.
		"""
		sys.path.append( path )
		for root, dirs, files in os.walk( path ):
			for file in files:
				if file == 'plugin.py':
					if None != restrict:
						name = root.replace( path, '' )[1:]
						if name not in restrict:
							continue
					import_path = root.replace( path, '' )[1:] + '/plugin'
					self.plugins[name] = __import__( import_path, None, None, [''] )
					for hook in self.plugins[name].hooks:
						if not self.hooks.has_key( hook ):
							self.hooks[hook] = []
						self.hooks[hook].append( name )

	def order_plugins ( self, order ):
		"""
		Attempt to put loaded plugins in a given order.
		"""
		if None != order:
			for index,hook in self.hooks.items():
				new_plugins = []
				for plugin in order:
					if plugin in hook:
						new_plugins.append( plugin )
				self.hooks[index] = new_plugins

	def get_plugins_by_hook ( self, hook ):
		"""
		Get all the needed plugins, in order, for a hook.
		"""
		plugins = []
		if self.hooks.has_key( hook ):
			for plugin in self.hooks[hook]:
				plugins.append( self.plugins[plugin] )
		return plugins
	
	def configure_plugins ( self, bot_path, config ):
		"""
		Attempt to configure loaded plugins.
		"""
		for name, plugin in self.plugins.items():
			try:
				if False == plugin.init( bot_path, config ):
					del self.plugins[name]
			except AttributeError:
				continue