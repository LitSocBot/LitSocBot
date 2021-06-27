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


class Crossword():
	def __init__(self):
		self.url = 'https://raw.githubusercontent.com/doshea/nyt_crosswords/master'
		self.year = str(rd.randint(1976, 2017))
		self.months = []
		for x in os.listdir('nyt_crossword' + '/' + self.year):
			self.months.append(x)
		self.month = rd.choice(self.months)
		self.days = []
		for x in os.listdir('nyt_crossword' + '/' + self.year + '/' + self.month):
			self.days.append(x)
		self.day = rd.choice(self.days)
		self.url = self.url + '/' + self.year + '/' + self.month + '/' + self.day
		self.response = requests.get(self.url)
		self.json_data = json.loads(self.response.text)
		self.across_answers = self.json_data["answers"]["across"]
		self.down_answers = self.json_data["answers"]["down"]
		self.author = self.json_data["author"]
		self.across_clues = self.json_data["clues"]["across"]
		self.down_clues = self.json_data["clues"]["down"]
		self.copyright = self.json_data["copyright"]
		self.date = self.json_data["date"]
		self.dow = self.json_data["dow"]
		self.grid = self.json_data["grid"]
		self.gridnums = self.json_data["gridnums"]
		self.rows = int(self.json_data["size"]["rows"])
		self.columns = int(self.json_data["size"]["cols"])
		self.blank = np.zeros((self.rows*30 + (self.rows +1)*3, self.rows*30 + (self.rows +1)*3, 3), dtype='uint8')
		self.blank[:,:] = 255, 255, 255
		self.dic_down = {}
		self.dic_across = {}
		self.dic_down_clues = {}
		self.dic_across_clues = {}
		for i in range(len(self.down_clues)):
			elem = self.down_clues[i]
			index = elem.find(". ")
			num = int(elem[:index])
			# self.down_answers[i] = elem[0:index+2] + self.down_answers[i]
			self.dic_down[num] = self.down_answers[i]
			self.dic_down_clues[num] = ". ".join(elem.split(". ")[1:])
		for i in range(len(self.across_clues)):
			elem = self.across_clues[i]
			index = elem.find(". ")
			# self.across_answers[i] = elem[0:index+2] + self.across_answers[i]
			num = int(elem[:index])
			self.dic_across[num] = self.across_answers[i]
			self.dic_across_clues[num] = ". ".join(elem.split(". ")[1:])
		for i in range(0, self.rows+1):
			cv.rectangle(self.blank, (33*i, 0), (33*i + 3, self.rows*30 + (self.rows +1)*3), (128, 128, 128), thickness=-1)
			cv.rectangle(self.blank, (0, 33*i), (self.rows*30 + (self.rows +1)*3, 33*i + 3), (128, 128, 128), thickness=-1)
		for count, value in enumerate(self.grid):
			row = count % self.rows
			col = count // self.rows
			if(value == '.'):
				cv.rectangle(self.blank, (row*33 + 3, col*33 + 3), (row*33 + 33, col*33 + 33), (0, 0, 0), thickness=-1)
		for count, value in enumerate(self.gridnums):
			row = count % self.rows
			col = count // self.rows
			if value == 0:
				pass
			else:
				cv.putText(self.blank, str(value), (row*33 + 4, col*33 + 12), cv.FONT_HERSHEY_PLAIN, 0.6, (0, 0, 0), thickness=1)	
		cv.imwrite('crossword.jpg', self.blank)

	def enterAnswer(self, answer, val, choice):
		for count, value in enumerate(self.gridnums):
			row = count % self.rows
			col = count // self.rows
			if val == value:
				for letter in answer:
					cv.putText(self.blank, str(letter), (row*33 + 13, col*33 + 26), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), thickness = 2)
					if choice.lower() == 'a':
						row = row+1
					else:
						col = col + 1
				cv.imwrite('crossword.jpg', self.blank)
				return True

	def checkAnswer(self, answer, val, choice):
		if choice.lower() == 'a':
			# checkString = str(val) + ". " + answer	#"2. ANS" ["2. CAT" "12. ANSWER"]
			if self.dic_across[val] == answer:	
				return True
			else:
				return False
		elif choice.lower() == 'd':
			if self.dic_down[val] == answer:	
				return True
			else:
				return False
		else:
			return False

	def giveClues(self, val, choice):
		val = int(val)
		if choice.lower() == 'a':
			return self.dic_across_clues.get(val, "Could not find any clue for that position")
		elif choice.lower() == 'd':
			return self.dic_down_clues.get(val, "Could not find any clue for that position")