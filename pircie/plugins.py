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
	plugin_objects = {}

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
					name = file[:-3]
					if None != restrict:
						if name not in restrict:
							continue
					import_path = root.replace( path, '' )[1:] + "/" + name
					module = __import__( import_path, None, None, [''] )
					self.plugins[name] = module

	def plugin_chain ( self, chain ):
		"""
		Set up the hooks according to the given chain.
		"""
		for pair in chain:
			name,plugin = pair
			if not self.plugins.has_key( plugin ):
				print 'ERROR: Plugin "%s" not loaded!' % plugin
			else:
				self.plugin_objects[name] = self.plugins[plugin].Plugin()
				for hook in self.plugin_objects[name].hooks:
					if not self.hooks.has_key( hook ):
						self.hooks[hook] = []
					self.hooks[hook].append( name )
	
	def configure_plugins ( self, bot_path, config ):
		"""
		Attempt to configure loaded plugins.
		"""
		for name,plugin in self.plugin_objects.items():
			try:
				if False == plugin.configure( bot_path, config, name ):
					self.drop_plugin( name )
			except AttributeError:
				continue
			except Exception, e:
				print "ERROR: Problem configuring plugin %s: %s" % ( name, e )
				self.drop_plugin( name )
	
	def drop_plugin ( self, name ):
		"""
		Remove a plugin object by name and all of it's hooks.
		"""
		if name in self.plugin_objects:
			del self.plugin_objects[name]
			for index,hook in self.hooks.items():
				try:
					self.hooks[index].remove( name )
				except ValueError:
					continue
					
	def get_plugins_by_hook ( self, hook ):
		"""
		Get all the needed plugins, in order, for a hook.
		"""
		plugins = []
		if self.hooks.has_key( hook ):
			for name in self.hooks[hook]:
				plugins.append( self.plugin_objects[name] )
		return plugins