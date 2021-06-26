from typing import Optional
import discord as dc
import os
from discord.ext.commands.core import command
import requests
import json
# import CowsAndBulls
import feedparser
import random

from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = "ODU2NTg0MjMyNDczMTk4NjA5.YNDKOw.aOphgguom5abLFC9hUEgBS5EVz8"

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))

@bot.command(name='anagram', help='Gets possible anagram for the word')
async def Anagram(ctx, choice : str):
    response = requests.get("http://www.anagramica.com/all/" + choice)
    json_data = json.loads(response.text)
    words = "\n".join(json_data["all"])
    await ctx.reply(ctx.author.mention +" Here are the possible anagrams\n" + words)

@bot.command(name='wordswith', help='Gets possible words with the letters')
async def Anagram(ctx, choice : str):
    response = requests.get("http://www.anagramica.com/all/:" + choice)
    json_data = json.loads(response.text)
    words = "\n".join(json_data["all"])
    await ctx.reply(ctx.author.mention +" Here are the possible words with those letters\n" + words)

@bot.command(name='isthere', help='Tells if a word is there or not')
async def Anagram(ctx, choice : str):
    response = requests.get("http://www.anagramica.com/lookup/" + choice)
    json_data = json.loads(response.text)
    value = json_data["found"]
    if(value):
        await ctx.reply(ctx.author.mention + "Yikes")
    else:
        await ctx.reply(ctx.author.mention + "Nope :(\nTry looking for something else")
        
@bot.command(aliases = ['deb'], help = 'Get random debate topics')
async def debate(ctx):
    NewsFeed = feedparser.parse("https://www.createdebate.com/browse/debaterss/all/rss")
    number = random.randint(0,11)
    entry = NewsFeed.entries[number]    
    show = entry.title
    await ctx.reply("Here:\n"+show)

def generate_topic(category):
    f=open('topics_updated.txt','r')
    topics=f.read()
    f.close()
    lis=topics.split('\n')
    if category == 'all':
        return lis[random.randint(0,len(lis))]
    li=lis[lis.index(category):lis.index('*',lis.index(category))]
    i=random.randint(0,len(li))
    topic=li[i]
    return topic

@bot.command(name='debatopic', help='Generate a debate topic based on some category\nList of Categories:\ngeneral\neducation\nsociety\nenvironment\npolitics\nparenting\ntech\nhealthcare\nleisure\nfinance and politics\nhistory\nfun\nall')
async def deb(ctx, choice:str):
    response = generate_topic(choice)
    await ctx.reply(response)
bot.run(TOKEN)
