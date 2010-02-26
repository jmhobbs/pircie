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

import random

class Plugin:

	hooks = [ 'MESSAGE' ]

	fortunes = [
		"I want to know God's thoughts... the rest are details. -Albert Einstein",
		"100% of the shots you don't take don't go in. -Wayne Gretzky",
		"An eye for eye only ends up making the whole world blind. -M.K. Gandhi",
		"Whatever the mind can conceive and believe, the mind can achieve. -Dr. Napoleon Hill",
		"Neither a lofty degree of intelligence nor imagination nor both together go to the making of genius. Love, love, love, that is the soul of genius. -Wolfgang Amadeus Mozart",
		"You can have everything in life that you want if you just give enough other people what they want. -Zig Ziglar",
		"Keep away from people who try to belittle your ambitions. Small people always do that, but the really great make you feel that you, too, can become great. -Mark Twain",
		"Great works are performed, not by strength, but by perseverance. -Samuel Johnson",
		"I made this letter longer than usual because I lack the time to make it short. -Blaise Pascal"
	]

	def MESSAGE ( self, bot, user, channel, message ):
		if 'FORTUNE' == message:
			bot.try_say( random.sample( self.fortunes, 1 )[0] )