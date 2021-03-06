#!/usr/bin/env python2

import select
import socket
import re

#this is the main class for bokbot, on which you can build other bots
#check teimport remplatebot.py for an example of how it might be implemented

#there's no real documentation yet but there will be soon

class bokbot:
	def __init__(self):
		self.channel = ""

	def connect(self, server, port):
		self.server = server
		self.port = port

		self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.irc.connect((self.server, self.port))
	
	def login(self, nick, name):
		self.nick = nick
		self.name = name
		
		self.send("NICK", "%s" % (self.nick))
		self.send("USER", "%s %s server %s" % (self.nick, self.server, self.name))

	def join(self, channel):
		self.channel = channel
		self.send("JOIN", self.channel)

	def part(self, msg):
		self.channel = ""
		self.send("PART", "%s :%s" % (self.channel, msg))

	def send(self, cmd, content=None):
		if content is None:
			message = "%s\r\n" % (cmd)
		else:
			message = "%s %s\r\n" % (cmd, content)
		self.irc.send(message)
		print message.strip()

	def say (self, msg, destination="NULL"):
		if destination == "NULL":
			destination = self.channel

		self.send("PRIVMSG", destination + " :" + msg)

	def disconnect(self):
		self.irc.send("QUIT")
		self.irc.close()

	def receive(self,block=True,timeout=0):
		if(block): return self.irc.recv(4096)
		if len(select.select([self.irc], [], [],timeout)[0]): return self.irc.recv(4096)
		return None

	def find(self, data, str):
		return data.lower().find(str)

	def modeChange(self, user, mode):
		self.send("MODE", self.channel + " " + mode + " " + user)

	def kick(self, user, msg):
		self.send("KICK %s %s :%s" % (self.channel, user.rstrip(), msg))

	def ctcp(self, cmd):
		self.say("\x01%s\x01" % cmd)

	def me(self, msg):
		self.ctcp("ACTION " + msg)

	def main(self,block=True,timeout=0):
		data = self.receive(block,timeout)
		if(not data): return None
		print data.strip()
		if data.find('PING') != -1:
			tmp = re.search("PING :(\w{8})", data)
			if tmp is not None:	
				number = " :%s" % tmp.groups()[0].split()[0]
				self.send("PONG%s" % number, "")
			else:
				self.send("PONG", data.split()[1])
				
		return data