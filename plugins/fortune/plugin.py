# -*- coding: utf-8 -*-

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