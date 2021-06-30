import enum
from typing import Optional
import discord as dc
import os
from discord.ext.commands.core import command
import requests
import json
import re
from discord.ext import commands
from dotenv import load_dotenv
import random as rd
import cv2 as cv
import numpy as np

class GenCwd():
	def __init__(self):
		file = open("wordlist.txt", "w")
		file.close()
		self.wordlist = []
		self.len = 0
	
	def addWord(self, word):
		self.wordlist.append(word)
		self.len += 1
		self.computeCwd()
	
	def delWord(self, word):
		try:
			self.wordlist.remove(word)
			self.len -= 1
			self.computeCwd()
			return True
		except ValueError:
			return False
	
	def computeCwd(self):
		file = open("wordlist.txt", "w")
		for count, word in enumerate(self.wordlist):
			if count > 0:
				file.write("\n")
			file.write(word.upper())
		file.close()
		os.system("genxword -a -o \"Test\" wordlist.txt n")

# c = GenCwd()
# c.addWord("abcdef")
# c.addWord("hello")
# c.addWord("there")
# c.computeCwd()