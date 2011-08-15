#!/usr/bin/env python2

import socket

#this is the main class for bokbot, on which you can build other bots
#check templatebot.py for an example of how it might be implemented

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

	def send(self, cmd, content=None):
		if content is None:
			message = "%s\r\n" % (cmd)
		else:
			message = "%s %s\r\n" % (cmd, content)
		self.irc.send(message)
		print message

	def say (self, msg, destination="NULL"):
		if destination == "NULL":
			destination = self.channel

		self.send("PRIVMSG", destination + " :" + msg)

	def disconnect(self):
		self.irc.send("QUIT")
		self.irc.close()

	def receive(self):
		return self.irc.recv(4096)

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

	def main(self):
		data = self.receive()
		print data
		if data.find('PING') != -1:
			self.send("PONG", data.split()[1])
		return data
