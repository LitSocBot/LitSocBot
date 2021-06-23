import os
import requests
import json

def get_anagram(choice : str):
    response = requests.get("http://www.anagramica.com/all/" + choice)
    json_data = json.loads(response.text)
    words = json_data["all"]
    for word in words:
        print(word)
#hello there
# webhook commit
get_anagram("pta")
