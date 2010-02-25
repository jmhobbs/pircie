# -*- coding: utf-8 -*-

"""
This plugin is an example, and not very useful. It aborts processing on all
messages it recieves. Effectively "blackholing" them for the rest of the plugin
chain.
"""

hooks = [ 'MESSAGE', 'WHISPER' ]

def MESSAGE ( bot, user, channel, message ):
	return False

def WHISPER ( bot, user, message ):
	return False