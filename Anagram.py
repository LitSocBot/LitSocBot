import requests
import json

base_url = "http://www.anagramica.com/"

def getWordswith(choice):
    url = base_url + "all/:" + choice
    response = requests.get(url)
    json_data = json.loads(response.text)
    words = "\n".join(json_data["all"])
    return words

def isThere(choice):
    url = base_url + "lookup/" + choice
    response = requests.get(url)
    json_data = json.loads(response.text)
    value = json_data["found"]
    return value

def getAnagrams(choice):
    url = base_url + "best/:" + choice
    response = requests.get(url)
    json_data = json.loads(response.text)
    words = "\n".join(json_data["best"])
    return words