# -*- coding: utf-8 -*-

from xml.dom.minidom import parseString
import socket
from urllib import urlencode
from urllib2 import Request, urlopen, URLError, HTTPError

class Plugin:

	hooks = [ 'ATME' ]

	# Alternate sources you could try:
	#  http://ninjawords.com/definitions/get/[WORD]  (add POST variable 123 with no value)
	#  http://www.google.com/dictionary/json?callback=dict_api.callbacks.id100&q=[WORD]&sl=en&tl=en&restrict=pr%2Cde&client=te
	url = "http://services.aonaware.com/DictService/DictService.asmx/DefineInDict"

	def __init__ ( self ):
		# Set the timeout to something reasonable
		socket.setdefaulttimeout( 5 )

	def ATME ( self, bot, user, channel, message ):
		print message
		if 'WEBDEFINE' == message.split( ' ' )[0]:
			define = " ".join( message.split( ' ' )[1:] )
			
			data = urlencode( { 'dictId': 'wn', 'word': define } )
			request = Request( "%s?%s" % ( self.url, data ) )

			try:
				response = urlopen( request )
			except HTTPError, e:
				bot.try_say( 'The definition server returned an error code: %d' % e.code )
			except URLError, e:
				print 'We failed to reach a server.'
				bot.try_say( 'Failed to reach the definition server: %s' % e.reason )
			else:
				dom = parseString( response.read() )
				try:
					# TODO Cache this response locally?
					bot.try_say( "%s: %s" % ( define, dom.childNodes[0].getElementsByTagName( "Definitions" )[0].getElementsByTagName( "Definition" )[0].getElementsByTagName( "WordDefinition" )[0].childNodes[0].data ) )
					return False
				except:
					bot.try_say( "No definition found for '%s'." % define )