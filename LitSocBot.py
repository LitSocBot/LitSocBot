from typing import Optional
import discord as dc
import os
from discord.ext.commands.core import command
import requests
import json
from CowsAndBulls import CowsAndBulls
import Anagram as ana
import feedparser
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
from Crossword import Crossword
from CrosswordGen import GenCwd
from private import *
import urllib.request
import numpy as np
import cv2 as cv

load_dotenv()

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))

@bot.command(name='anagram', help='Gets possible anagram for the word')
async def Anagram(ctx, choice : str):
    await ctx.reply(ctx.author.mention +" Here are the possible anagrams\n" + ana.getAnagrams(choice))

@bot.command(name='wordswith', help='Gets possible words with the letters')
async def Anagram(ctx, choice : str):
    await ctx.reply(ctx.author.mention +" Here are the possible words with those letters\n" + ana.getWordswith(choice))

@bot.command(name='isthere', help='Tells if a word is there or not')
async def Anagram(ctx, choice : str):
    value = ana.isThere(choice)
    if(value):
        await ctx.reply(ctx.author.mention + "Yes")
    else:
        await ctx.reply(ctx.author.mention + "Nope :(\nTry looking for something else")

#Debate Bot Commands 
#Using discord bot subcommand feature
#primary command :will generate random debate topics
      
@bot.group(pass_context = True,help = 'Use addtop command (!debate addtop) to add a custom topic.')
async def debate(ctx):             
    NewsFeed = feedparser.parse("https://www.createdebate.com/browse/debaterss/all/rss")
    
    number = random.randint(0,11)  #there are only 12 debate topics in this api
    entry = NewsFeed.entries[number]    
    show = entry.title
    
    if ctx.invoked_subcommand is None:
        await ctx.reply("Here:\n"+show) 
    else:
        print("what")  

#secondary command: will add topics given by the user to the category 'mods'

@debate.group(pass_context =True)    
async def addtop(ctx,*,choice):   
    with open('topics_updated.txt','r') as f:
        contents = f.readlines()
        choice = choice + "\n"
        contents.insert(146,choice)

    with open('topics_updated.txt','w') as f:
        contents = "".join(contents)
        f.write(contents)
        
    await ctx.reply("The topic has been added.")


#searching through a text file to generate debate topics under specific categories
loc=''            #loc = list of contents

lot= ['*','all','general', 'education', 'society', 'environment', 'politics', 'parenting', 'tech', 'healthcare', 'leisure', 'finance and politics', 'history', 'fun','mods']

for term in lot:        #goes through list of topics and adds these topics to the string loc
    if term =='*':
         continue
    loc=loc+'\n'+''.join(term)

def generate_topic(category):     
    f=open('topics_updated.txt','r')
    topics=f.read()    
    f.close()

    #moving the topics from the text file to a list
    lis=topics.split('\n')     
    if category == 'all':
        topic=lis[random.randint(0,len(lis))]
        if((topic not in lot)):
            return topic
    
    #returns topics from specific categories
    li=lis[lis.index(category):lis.index('*',lis.index(category))]
    i=random.randint(0,len(li))
    topic=li[i]
    return topic

@bot.command(name='debatopic', help='Generate a debate topic based on some category\nList of Categories:'+loc)
async def deb(ctx, choice:str):
    response = generate_topic(choice)
    await ctx.reply(response)
    

@bot.command(name='startcwd', help='Generates a random crossword')
async def cwd(ctx):
    global c
    c = Crossword()
    await ctx.reply(file=discord.File('crossword.jpg'))
    acrossclues = "\n".join(c.across_clues)
    downclues = "\n".join(c.down_clues)
    acrossClues = acrossclues.replace("_", "\_")
    downClues = downclues.replace("_", "\_")
    await ctx.reply("**Clues**:\n**Across**:\n" + acrossClues)
    await ctx.reply("**Down**:\n" + downClues)
    for ind in c.dic_across.keys():
        print(ind, " : ", c.dic_across[ind])
    for ind in c.dic_down.keys():
        print(ind, " : ", c.dic_down[ind])

    
@bot.command(name='answercwd', help='To answer a crossword')
async def ans(ctx, val : int, choice : str, answer : str):
    # across = (choice == 'a')
    answer = answer.upper()
    if(c.checkAnswer(answer, val, choice)):
        await ctx.reply("Correct Answer")
        c.enterAnswer(answer, val, choice)
        await ctx.reply(file=discord.File('crossword.jpg'))
    else:
        await ctx.reply("Wrong Answer")

@bot.command(name='clues', help='Gives clues for specified grid number and direction')
async def clues(ctx, *args):
    if len(args) == 1:
        choice = args[0].lower()
        acrossclues = "\n".join(c.across_clues)
        downclues = "\n".join(c.down_clues)
        acrossClues = acrossclues.replace("_", "\_")
        downClues = downclues.replace("_", "\_")
        if choice == 'all':
            await ctx.reply("**Across**:\n" + acrossClues)
            await ctx.reply("**Down**:\n" + downClues)
        if choice == 'down':
            await ctx.reply("**Down**:\n" + downClues)
        if choice == 'across':
            await ctx.reply("**Across**:\n" + acrossClues)
    else:
        response = ""
        for i in range(len(args) // 2):
            clue = c.giveClues(args[2*i], args[2*i+1])
            response = response + args[2*i] + args[2*i+1] + ". " + clue + "\n"
        await ctx.reply(response)


@bot.command(name='createcwd', help='Resets the word list to generate a new crossword')
async def gencwd(ctx):
    global crwd
    crwd = GenCwd()
    await ctx.reply("Word list succesfully reset")

@bot.command(name='addword', help='To add a word to the word list which generates the crossword')
async def addword(ctx, *args):
    for word in args:
        crwd.addWord(word)
    if len(args) > 1:
        await ctx.reply(", ".join(args) + " have been added to the list")
    else:
        await ctx.reply(", ".join(args) + " has been added to the list")

@bot.command(name='delword', help='To remove a word from the word list')
async def delword(ctx, word):
    deleted = crwd.delWord(word)
    if deleted:
        await ctx.reply(word + " has been deleted from the word list")
    else:
        await ctx.reply("No such word in the list")
        
@bot.command(name='showcwd', help='Generates a crossword using the word in the word list')
async def showcwd(ctx):
    # crwd.computeCwd()
    await ctx.reply(file=discord.File('Test_grid.png'))
    file = open('Clues.txt', 'r')
    content = file.read()
    file.close()
    await ctx.reply(content)

@bot.command(name='showkey', help='Displays the grid with key to the crossword')
async def showkey(ctx):
    await ctx.reply(file=discord.File('Test_key.png'))

@bot.command(name='xkcd', help='Displays a random xkcd comic strip')
async def xkcdcomic(ctx):
    number = str(random.randint(1, 2484))
    url = "https://xkcd.com/" + number + "/info.0.json"
    pg = requests.get(url)
    json_data = json.loads(pg.text)
    img = json_data["img"]
    urllib.request.urlretrieve(img, "xkcd.png")
    await ctx.reply(file=discord.File('xkcd.png'))

@bot.command(name='startcb', help='Starts a new Cow Bulls game')
async def startcowbull(ctx, dig : int):
    global cb 
    cb = CowsAndBulls()
    cb.active=True
    cb.digits=dig
    cb.number=cb.makeRandom(cb.digits)
    print(cb.number)
    await ctx.reply('Game started\nPlease guess a {}-digit number'.format(cb.digits))

@bot.command(name='guesscb', help='To make a guess')
async def guesscowbull(ctx, num : str):
    if(cb.active):
        bulls, cows = CowsAndBulls.compareNumbers(cb.number, num)
        if bulls == cb.digits:
            await ctx.reply('Cows : {}\nBulls : {}\nYou win!!'.format(cows, bulls))
            cb.active=False
        elif bulls == -1:
            await ctx.reply('Please enter a {}-digit number'.format(cb.digits))
        else:
            await ctx.reply('Cows : {}\nBulls : {}'.format(cows, bulls))

@bot.command(name='stopcb', help='To make a guess')
async def stopCowBull(ctx):
    cb.active=False
    await ctx.reply('Game stopped successfully.\n{} was the answer'.format(cb.number))


#this command gives info on movies by searching through their titles
@bot.command(help = 'Get movie details')
async def movies(ctx,*,choice):

    final = choice.replace(" ","+")
    url = "http://www.omdbapi.com/?t=" + final + "&apikey=5a70a732"

    response = requests.get(url)
    json_data = json.loads(response.text)   
    
    if json_data["Response"] == "True":
        
        movie_name = json_data["Title"]
        runtime = json_data["Runtime"]
        rating = json_data["imdbRating"]
        genre = json_data["Genre"]
        director = json_data["Director"]
        poster = json_data["Poster"]
        
        if poster != "N/A":           
            urllib.request.urlretrieve(poster, "poster.jpg")
            file = discord.File('poster.jpg')

            message = discord.Embed(title = movie_name, color = 0xFFFFFF )
            message.add_field(name = "Genre", value = genre, inline= False)
            message.add_field(name= "Director", value= director, inline= False)
            message.add_field(name= "Runtime", value= runtime, inline= False)
            message.add_field(name= "IMDb Rating", value= rating,inline= False)
            message.set_image(url = "attachment://poster.jpg")
            
            await ctx.reply(file = file,embed = message)

        elif poster == "N/A":

            message = discord.Embed(title = movie_name, color = 16777215 )
            message.add_field(name = "Genre", value = genre, inline= False)
            message.add_field(name= "Director", value= director,inline= False)
            message.add_field(name= "Runtime", value= runtime,inline= False)
            message.add_field(name= "IMDb Rating", value= rating,inline= False)

            await ctx.reply(embed = message)

    else :
        message = discord.Embed(title = "Error", description = "Either the info isn't available or the spelling is wrong.", color = 15158332 )

        await ctx.reply(embed = message)


#a wordsearch that creates grids on random words
@bot.command(name='ws', help= 'Generate a 10x10 wordsearch')
async def wordsearch_(ctx):
    response=requests.get('https://random-word-api.herokuapp.com/word?number=20')
    l=response.json()

    with open ('w.txt', 'w') as w:
        c=0
        for wor in l:
            if c==10:
                break
            if(len(wor)<11):
                w.write(wor+'\n')  
                c+=1

    os.system('python word_search.py')

    s=''
    #extracting solution from a file
    with open('sol.txt', 'r') as sol: 
        for line in sol:
            s=s+''.join(line)

    await ctx.reply(s)
    
    #creating a blank 10x10 grid
    rows=10
    blank = np.zeros((rows*30 + (rows +1)*3, rows*30 + (rows +1)*3, 3), dtype='uint8')
    blank[:,:] = 255, 255, 255

    for i in range(0, rows+1):
        cv.rectangle(blank, (33*i, 0), (33*i + 3, rows*30 + (rows +1)*3), (128, 128, 128), thickness=-1)
        cv.rectangle(blank, (0, 33*i), (rows*30 + (rows +1)*3, 33*i + 3), (128, 128, 128), thickness=-1)

    cv.imwrite('wordsearch.jpg', blank)
    s=''
    with open('ws.txt', 'r') as f:
        st=f.read()
    
    ls=list(st)

    count=0
    
    #putting letters in the grid
    for i in range(len(ls)):
        row=count%10
        col=count//10
        cv.putText(blank, str(ls[i]), (row*33 +13, col*33 + 26), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), thickness = 2)
        count+=1
        cv.imwrite('wordsearch.jpg', blank)
    
    await ctx.reply(file=discord.File('wordsearch.jpg'))


#this command gives info on books related to IT/CSE by searching through their titles
@bot.command(help = 'Get IT books info')
async def itbooks(ctx,*,choice):

    final = choice.replace(" ","+")
    url = "https://api.itbook.store/1.0/search/"+ final

    response = requests.get(url)
    json_data = json.loads(response.text)

    bookdesc = " "

    for bookname in json_data["books"]: 
        booktitle = bookname["title"]
        description = bookname["subtitle"]       
        link = bookname["url"]

        bookdesc += "**"+booktitle+"**" + " : " + description + "\n" + "<" + link + ">" + "\n" 

    if len(json_data["books"]) != 0 :
        await ctx.reply(bookdesc)

    else :
        message = discord.Embed(title = "Error", description = "Either the info isn't available or the spelling is wrong.", color = 15158332 )

        await ctx.reply(embed = message)

        


bot.run(TOKEN)