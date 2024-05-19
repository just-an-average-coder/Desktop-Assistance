import speech_recognition as sr
import pyttsx3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import sys
import os

INTRODUCTION = "hello, i am rupaali, who are you?"


r = sr.Recognizer()
engine = pyttsx3.init()

web_driver_path = "./chromedriver.exe"
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
service = Service(executable_path=web_driver_path)

def rick_roll():

    try:
        driver = webdriver.Chrome(options=chrome_options, service=service)
        driver.get("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        time.sleep(1)
        play_button = driver.find_element(By.CSS_SELECTOR, ".ytp-left-controls button")
        play_button.click()
    except:
        return
    
def search_google(text):

    try:
        driver = webdriver.Chrome(options=chrome_options, service=service)
        driver.get("https://google.com")
        time.sleep(1)
        search_bar = driver.find_element(By.CLASS_NAME, "gLFyf")
        search_bar.send_keys(text)
        time.sleep(.2)
        search_bar.send_keys(Keys.ENTER)
    except:
        return
    
def search_youtube(text):

    try:
        driver = webdriver.Chrome(options=chrome_options, service=service)
        driver.get("https://youtube.com")
        time.sleep(1)
        search_bar = driver.find_element(By.NAME, "search_query")
        search_bar.send_keys(text)
        time.sleep(.2)
        search_bar.send_keys(Keys.ENTER)
  
    except:
        return

def introduce():

    say(INTRODUCTION)
    try:
        with sr.Microphone() as source:
            # read the audio data from the default microphone
            print("Listining...")
            r.adjust_for_ambient_noise(source=source, duration=0.5)
            audio_data = r.listen(source, phrase_time_limit=10)
            print("Recognizing...")
            # convert speech to text
            text = r.recognize_google(audio_data).lower()
            print(text)
            global name
            name = text
    except sr.UnknownValueError:
        introduce()

def say(text):

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 150)

    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":

    name = ""
    introduce()

    while True:
        try:
            with sr.Microphone() as source:
                # read the audio data from the default microphone
                print("Listining...")
                r.adjust_for_ambient_noise(source=source, duration=0.5)
                audio_data = r.listen(source, timeout=2, phrase_time_limit=5)
                print("Recognizing...")
                # convert speech to text
                text = r.recognize_google(audio_data).lower()
                print(text)

                if "quit" in text or "exit" in text:
                    say(f"bye, see you later {name}")
                    sys.exit(0)

                elif text == "rick roll":
                    rick_roll()

                elif "google" in text:
                    text = text.replace("google", "").strip()
                    search_google(text)
                    say(f"here is the result of the search {text}")

                elif "youtube" in text:
                    text = text.replace("youtube", "").strip()
                    search_youtube(text)

        except sr.WaitTimeoutError:
            continue

        except sr.UnknownValueError:
            print("error recognizing voice")
            r = sr.Recognizer()
            continue


    