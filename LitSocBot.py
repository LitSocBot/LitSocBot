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
import urllib.request
import numpy as np
import cv2 as cv

load_dotenv()
TOKEN = "ODU2NTg0MjMyNDczMTk4NjA5.YNDKOw.aOphgguom5abLFC9hUEgBS5EVz8"

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
        
@bot.group(pass_context = True)
async def debate(ctx):
    NewsFeed = feedparser.parse("https://www.createdebate.com/browse/debaterss/all/rss")
    number = random.randint(0,11)
    entry = NewsFeed.entries[number]    
    show = entry.title
    if ctx.invoked_subcommand is None:
        await ctx.reply("Here:\n"+show) 
    else:
        print("what")              

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

loc=''
lot= ['*','all','general', 'education', 'society', 'environment', 'politics', 'parenting', 'tech', 'healthcare', 'leisure', 'finance and politics', 'history', 'fun','mods']
for term in lot:
    if term =='*':
         continue
    loc=loc+'\n'+''.join(term)
def generate_topic(category):
    f=open('topics_updated.txt','r')
    topics=f.read()    
    f.close()
    lis=topics.split('\n')
    if category == 'all':
        topic=lis[random.randint(0,len(lis))]
        if((topic not in lot)):
            return topic
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
    await ctx.reply(", ".join(args) + " have been added to the list")

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

@bot.command(help = 'get movie details')
async def movies(ctx,*,choice):
    final = choice.replace(" ","+")
    url = "http://www.omdbapi.com/?t=" + final + "&apikey=5a70a732"
    response = requests.get(url)
    json_data = json.loads(response.text)
    p1 = json_data["Title"]
    p2 = json_data["Runtime"]
    p3 = json_data["imdbRating"]
    p4 = json_data["Genre"]
    p5 = json_data["Director"]
    p6 = json_data["Poster"]
    
    urllib.request.urlretrieve(p6, "poster.jpg")
    await ctx.reply(f"\nTitle: {p1}\nGenre: {p4}\nDirector:{p5}\nRuntime: {p2}\nimdb rating:{p3}",file=discord.File('poster.jpg') )

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
    # await ctx.reply('no thanks')
    s=''
    with open('sol.txt', 'r') as sol:
        for line in sol:
            s=s+''.join(line)
    await ctx.reply(s)
    
    
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
    # ls=list(s)
    # ls.remove('\n')
    # print(ls)
    ls=list(st)

    count=0

    for i in range(len(ls)):
        row=count%10
        col=count//10
        cv.putText(blank, str(ls[i]), (row*33 +13, col*33 + 26), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), thickness = 2)
        count+=1
        cv.imwrite('wordsearch.jpg', blank)
    # with open('ws.txt','r') as ws:
    #     for line in ws:
    #         s1=s1 + ''.join(line)
    await ctx.reply(file=discord.File('wordsearch.jpg'))

@bot.command(help = 'get IT books')
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

    await ctx.reply(bookdesc)

bot.run(TOKEN)