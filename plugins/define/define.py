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

# We need to get sdictviewer into the path, part of the price we pay to be plugins
import os.path
import sys
sys.path.append( os.path.dirname(__file__) )

import sdictviewer.formats.dct.sdict as sdict
import sdictviewer.dictutil

class Plugin:

	hooks = [ 'ATME' ]

	dictionary = None

	def configure ( self, path, config ):
		try:
			if os.path.isabs( config.get( 'define', 'dictionary' ) ):
				self.dictionary = sdict.SDictionary( config.get( 'define', 'dictionary' ) )
			else:
				self.dictionary = sdict.SDictionary( path + config.get( 'define', 'dictionary' ) )
			self.dictionary.load()
		except:
			return False

	def ATME ( self, bot, user, channel, message ):
		if 'DEFINE' == message.split( ' ' )[0]:
			start_word = " ".join( message.split( ' ' )[1:] )
			found = False
			for item in self.dictionary.get_word_list_iter( start_word ):
				try:
					if start_word == str( item ):
						instance, definition = item.read_articles()[0]
						bot.try_say( "%s: %s" % ( item, definition ) )
						found = True
						break
				except:
					continue
			if not found:
				bot.try_say( "No definition for '%s'." % start_word )
			return not found