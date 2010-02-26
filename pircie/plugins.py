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
				if file[-3:] == '.py':
					if None != restrict:
						name = file[:-3]#root.replace( path, '' )[1:]
						if name not in restrict:
							continue
					import_path = root.replace( path, '' )[1:] + "/" + name
					module = __import__( import_path, None, None, [''] )
					self.plugins[name] = module.Plugin()
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
				if False == plugin.configure( bot_path, config ):
					self.drop_plugin( name )
			except AttributeError:
				continue
	
	def drop_plugin ( self, name ):
		"""
		Remove a plugin by name and all of it's hooks.
		"""
		if name in self.plugins:
			del self.plugins[name]
			for index,hook in self.hooks.items():
				try:
					self.hooks[index].remove( name )
				except ValueError:
					continue