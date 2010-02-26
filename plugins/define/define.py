# -*- coding: utf-8 -*-

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