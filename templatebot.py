#!/usr/bin/env python2

from bokbot import bokbot
import random

class templatebot(bokbot):

	#def __init__(self):
		#stuff to do upon initialization
	
	def mainLoop(self):
		#the main loop
		
		while(True):
			#grab data
			data = self.main()
		
			#bot-specific stuff
			if data.find("PRIVMSG") != -1:
				#the nick of the person who sent the message
				nick = data.split('!')[0].replace(':', '')	
				#the channel the message was sent to (channel, pm, etc)
				destination = data.split(' ')[2]
				#the body of the message that was sent
				message = data.split(':')[2]
				#the first word of a message - use it if you want to make a command like !dino
				cmd = message.split(' ')[0]
				#space-delimited list of the words after the first word, to be used as arguments in conjunction with cmd
				args = message.split(' ')
				args.pop(0)
				
				if destination == self.nick:
					destination = nick
					#respond to private messages
					
				else:
					#respond to stuff in the current channel
					if self.find(data, "example") != -1:
						self.say("i am responding to the example")
			
			elif data.find("JOIN :" + self.channel) != -1:
				nick = data.split('!')[0].replace(':', '') 
                                destination = data.split(' ')[2].replace(':', '').rstrip()
				#respond to channel joins	

#the good stuff
#connect to a channel, start the main loop
bot = templatebot()
bot.connect("irc.freenode.net", 6667)
#          nick,     name
bot.login("bokbot", "bokbot")
bot.join("#bokland")
bot.mainLoop()
