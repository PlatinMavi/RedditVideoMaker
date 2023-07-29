import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import os
import pyttsx3

def ScrapePostContent(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html,"html.parser")

    title = soup.find("div",{"slot":"title"}).text.strip()
    author = soup.find("faceplate-tracker", {"noun":"user_profile"}).text.strip()

    textContent = ""
    content = soup.find("div",{"slot":"text-body"}).find("div").find_all("p")
    for x in content:
        textContent = textContent+x.text.strip()
    return(author,title,textContent)

def ToSpeech(content):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # You can change the voice index to select different voices. 
    # In this case, using 1 for a male voice.
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 150)
    
    text = content[1] + " " + content[2]
    # engine.say(text)
    engine.save_to_file(text, "example.mp3")
    engine.runAndWait()

result = ScrapePostContent("https://www.reddit.com/r/tifu/comments/a99fw9/tifu_by_buying_everyone_an_ancestrydna_kit_and/")
ToSpeech(result)
print("complete")