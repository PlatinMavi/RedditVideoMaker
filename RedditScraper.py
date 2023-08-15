import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import pyttsx3
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip
from moviepy.video.tools.drawing import color_gradient
from moviepy.config import change_settings
import random
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})
#PLEASE CUSTOMIZE THIS FOR PERSONAL USAGE

def screenShotPost(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("start-maximized")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, "shreddit-post")))
    post = driver.find_element(By.TAG_NAME, 'shreddit-post')
    post.screenshot(filename="./temp/Post.png")
    driver.quit()


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
    engine.setProperty('rate', 175)
    
    text = content[1] + " " + content[2]
    engine.save_to_file(text, "./temp/TextToSpeech.mp3")
    engine.runAndWait()

    return content[1]


def ToSpeechGTTS(content):
    text = content[1] + " " + content[2]
    tts = gTTS(text, lang='en', tld="com.au")
    tts.save("./temp/TextToSpeech.mp3")
    return content[1]


#VIDEO MAKER
def GetVideoPNG(name,screenshotpath = "./temp/Post.png",input_video_path = "./BackGrounds/SubwaySurfer.mp4", input_audio_path = "./temp/TextToSpeech.mp3"):
    output_path = f"./Output/{name}.mp4"
    video_clip = VideoFileClip(input_video_path)
    audio_clip = AudioFileClip(input_audio_path)

    max_start_time = video_clip.duration - audio_clip.duration
    start_time = random.uniform(0, max_start_time)
    cropped_video = video_clip.subclip(start_time, start_time + audio_clip.duration)

    final_video = cropped_video.set_audio(audio_clip)
    final_video = final_video.volumex(0.8)

    png_image = ImageClip(screenshotpath)
    png_duration = final_video.duration  # Adjust the duration of the PNG to match the video
    png_image = png_image.set_duration(png_duration)

    # Calculate image width and height to fit with padding
    padding = 30  # Adjust as needed
    video_width, video_height = final_video.size
    image_width = video_width - 2 * padding
    image_height = png_image.h * image_width // png_image.w

    png_image = png_image.resize(width=image_width, height=image_height)

    # Position the PNG image with padding from the corner of the screen
    x_pos = padding
    y_pos = (video_height - image_height - padding)/2
    positioned_image = png_image.set_position((x_pos, y_pos))

    # Overlay the positioned image onto the video
    final_video_with_overlay = CompositeVideoClip([final_video, positioned_image])

    final_video_with_overlay.write_videofile(output_path, codec='libx264')
    video_clip.close()
    audio_clip.close()

def Scrape(url):
    screenShotPost(url)
    result = ScrapePostContent(url)
    name = ToSpeechPYTTSX3(result)
    print("Scraped Succesfully")
    GetVideoPNG(name)

    os.remove("./temp/TextToSpeech.mp3")
    os.remove("./temp/Post.png")