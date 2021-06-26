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

# url = "https://raw.githubusercontent.com/doshea/nyt_crosswords/master/2000/06/24.json"
# response = requests.get(url)
# json_data = json.loads(response.text)
# count = len(json_data["answers"]["across"]) + len(json_data["answers"]["down"])
# print(count)

class Crossword():
	def __init__(self):
		self.url = 'https://raw.githubusercontent.com/doshea/nyt_crosswords/master'
		self.year = str(rd.randint(1976, 2017))
		self.months = []
		for x in os.listdir('nyt_crosswords' + '/' + self.year):
			self.months.append(x)
		self.month = rd.choice(self.months)
		self.days = []
		for x in os.listdir('nyt_crosswords' + '/' + self.year + '/' + self.month):
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
