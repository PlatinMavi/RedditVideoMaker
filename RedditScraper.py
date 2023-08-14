import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import os
import pyttsx3
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip
from moviepy.video.tools.drawing import color_gradient
import random

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

def ToSpeechPYTTSX3(content):
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


def ToSpeechGTTS(content):
    text = content[1] + " " + content[2]
    tts = gTTS(text, lang='en', tld="com.au")
    tts.save("example.mp3")
    return text


#VİDEO MAKER
def GetVideoTXT(text_content, input_video_path = r"C:\Users\PC\Desktop\RedditVideoMaker\SubwaySurfer.mp4", input_audio_path = r"C:\Users\PC\Desktop\RedditVideoMaker\example.mp3", output_path = r"C:\Users\PC\Desktop\RedditVideoMaker\Output\output.mp4"):
    video_clip = VideoFileClip(input_video_path)
    audio_clip = AudioFileClip(input_audio_path)

    max_start_time = video_clip.duration - audio_clip.duration
    start_time = random.uniform(0, max_start_time)
    cropped_video = video_clip.subclip(start_time, start_time + audio_clip.duration)

    # Create a TextClip with the text content
    txt_clip = TextClip(text_content, fontsize=30, color='white', size=cropped_video.size)
    txt_clip = txt_clip.set_duration(cropped_video.duration)

    # Overlay the text onto the cropped video
    video_with_text = CompositeVideoClip([cropped_video.set_audio(audio_clip), txt_clip.set_pos(('center', 'bottom'))])

    video_with_text.write_videofile(output_path, codec='libx264', audio_codec='aac')

    video_clip.close()
    audio_clip.close()

def GetVideo(input_video_path = r"C:\Users\PC\Desktop\RedditVideoMaker\SubwaySurfer.mp4", input_audio_path = r"C:\Users\PC\Desktop\RedditVideoMaker\example.mp3", output_path = r"C:\Users\PC\Desktop\RedditVideoMaker\Output\output.mp4"):
    video_clip = VideoFileClip(input_video_path)
    audio_clip = AudioFileClip(input_audio_path)

    max_start_time = video_clip.duration - audio_clip.duration
    start_time = random.uniform(0, max_start_time)
    cropped_video = video_clip.subclip(start_time, start_time + audio_clip.duration)
    final_video = cropped_video.set_audio(audio_clip)
    final_video.write_videofile(output_path, codec='libx264')

    video_clip.close()
    audio_clip.close()


def Scrape(url):
    result = ScrapePostContent(url)
    text = ToSpeechGTTS(result)
    print("Scraped Succesfully")

    GetVideo()