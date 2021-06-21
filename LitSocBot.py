from typing import Optional
import discord as dc
import os
from discord.ext.commands.core import command
import requests
import json
import CowsAndBulls

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

bot.run(TOKEN)