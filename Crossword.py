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

# url = "https://raw.githubusercontent.com/doshea/nyt_crosswords/master/2000/06/24.json"
# response = requests.get(url)
# json_data = json.loads(response.text)
# count = len(json_data["answers"]["across"]) + len(json_data["answers"]["down"])
# print(count)

class Crossword():
	def __init__(self):
		self.url = "https://raw.githubusercontent.com/doshea/nyt_crosswords"
		self.year = str(rd.randint(1976, 2017))
		self.months = []
		for x in os.listdir('/home/vikhyath/Personal-Projects/LambdaStuff/nyt_crosswords' + '/' + self.year):
			self.months.append(x)
		self.month = rd.choice(self.months)
		self.days = []
		for x in os.listdir('/home/vikhyath/Personal-Projects/LambdaStuff/nyt_crosswords' + '/' + self.year + '/' + self.month):
			self.days.append(x)
		self.day = rd.choice(self.days)
		self.url = self.url + '/' + self.year + '/' + self.month + '/' + self.day
		self.response = requests.get(self.url)
		self.json_data = json.loads(self.response.text)
		self.across_answers = self.json_data["answers"]["across"]
		self.down_answers = self.json_data["answers"]["down"]
		self.author = self.json_data["author"]
		
