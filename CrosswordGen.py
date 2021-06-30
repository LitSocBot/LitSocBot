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
from bs4 import BeautifulSoup as bs

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
		file = open('Test_clues.txt', 'r')
		lines = file.readlines()
		file.close()
		file = open('Clues.txt', 'w')
		count = 0
		for line in lines:
			count += 1
			if count > self.len + 2:
				if line == 'Clues\n' or line == 'Across\n' or line == 'Down\n':
					file.write(line)
				else:
					word = line.split(". ")[1].rstrip("\n")
					page = requests.get("https://www.the-crossword-solver.com/word/" + word)
					if page.status_code == 200:
						soup = bs(page.content, features="lxml")
						text = soup.find_all('a')
						clue = text[7].get('title')
						clue = clue.replace('Crossword clue ', '')
						newline = line.split(". ")[0] + ". " + clue + "\n"
						file.write(newline)
					else:
						file.write(line)
		file.close()

# c = GenCwd()
# c.addWord("abcdef")
# c.addWord("hello")
# c.addWord("there")
# c.computeCwd()