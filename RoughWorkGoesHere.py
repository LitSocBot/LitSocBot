import os
import requests
import json
from bs4 import BeautifulSoup as bs
import urllib.request
from PIL import Image

def get_anagram(choice : str):
    response = requests.get("http://www.anagramica.com/all/" + choice)
    json_data = json.loads(response.text)
    words = json_data["all"]
    for word in words:
        print(word)
#hello there
# webhook commit
get_anagram("pta")

page = requests.get("https://www.the-crossword-solver.com/word/hello")
soup = bs(page.content, features="lxml")

for link in soup.find_all('a'):
    print(link.get('title'))
print('*' * 50)
text = soup.find_all('a')
clue = text[7].get('title')
print(clue)
clue = clue.replace('Crossword clue ', '')
print('*' * 50)
print(clue)

pg = requests.get("https://xkcd.com/613/info.0.json")
json = json.loads(pg.text)
img = json["img"]
urllib.request.urlretrieve(img, "xkcd.png")
img = Image.open("xkcd.png")
img.show()