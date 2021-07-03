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
from Generator import Crossword, Word

class GenCwd():
	def __init__(self):
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
		self.clue_list = []
		for word in self.wordlist:
			page = requests.get("https://www.the-crossword-solver.com/word/" + word)
			if page.status_code == 200:
				soup = bs(page.content, features="lxml")
				text = soup.find_all('a')
				clue = text[7].get('title')
				clue = clue.replace('Crossword clue ', '')
				hint = [word, clue]
				self.clue_list.append(hint)
			else:
				hint = [word, word]
				self.clue_list.append(hint)
		
		# a = Crossword(21, 21, '-', 5000, self.clue_list)
		# a.compute_crossword(2)
	
	def displaygrid(self):
		self.rows = 21
		blank = np.zeros((self.rows*30 + (self.rows +1)*3, self.rows*30 + (self.rows +1)*3, 3), dtype='uint8')
		blank[:,:] = 255, 255, 255
		for i in range(0, self.rows+1):
			cv.rectangle(blank, (33*i, 0), (33*i + 3, self.rows*30 + (self.rows +1)*3), (128, 128, 128), thickness=-1)
			cv.rectangle(blank, (0, 33*i), (self.rows*30 + (self.rows +1)*3, 33*i + 3), (128, 128, 128), thickness=-1)
		
c = GenCwd()
c.addWord("saffron")
c.addWord("hello")
c.addWord("there")
c.addWord("queen")
a = Crossword(21, 21, '-', 5000, tuple(c.clue_list))
a.compute_crossword(spins=20)
print(a.solution())
print(len(a.solution()))
print(tuple(c.clue_list))
# c.clue_list = ['saffron', 'The dried, orange yellow plant used to as dye and as a cooking spice.'], \
#     ['pumpernickel', 'Dark, sour bread made from coarse ground rye.'], \
#     ['leaven', 'An agent, such as yeast, that cause batter or dough to rise..'], \
#     ['coda', 'Musical conclusion of a movement or composition.'], \
#     ['paladin', 'A heroic champion or paragon of chivalry.'], \
#     ['syncopation', 'Shifting the emphasis of a beat to the normally weak beat.'], \
#     ['albatross', 'A large bird of the ocean having a hooked beek and long, narrow wings.'], \
#     ['harp', 'Musical instrument with 46 or more open strings played by plucking.'], \
#     ['piston', 'A solid cylinder or disk that fits snugly in a larger cylinder and moves under pressure as in an engine.'], \
#     ['caramel', 'A smooth chery candy made from suger, butter, cream or milk with flavoring.'], \
#     ['coral', 'A rock-like deposit of organism skeletons that make up reefs.'], \
#     ['dawn', 'The time of each morning at which daylight begins.'], \
#     ['pitch', 'A resin derived from the sap of various pine trees.'], \
#     ['fjord', 'A long, narrow, deep inlet of the sea between steep slopes.'], \
#     ['lip', 'Either of two fleshy folds surrounding the mouth.'], \
#     ['lime', 'The egg-shaped citrus fruit having a green coloring and acidic juice.'], \
#     ['mist', 'A mass of fine water droplets in the air near or in contact with the ground.'], \
#     ['plague', 'A widespread affliction or calamity.'], \
#     ['yarn', 'A strand of twisted threads or a long elaborate narrative.'], \
#     ['snicker', 'A snide, slightly stifled laugh.']
# a = Crossword(21, 21, '-', 5000, c.clue_list)
# a.compute_crossword(2)
# print(a.solution())
# print(len(a.solution()))
# print(c.clue_list)
# c.computeCwd()