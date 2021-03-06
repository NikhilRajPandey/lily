from bs4 import BeautifulSoup
from gtts import gTTS
from datetime import datetime
from re import sub
import speech_recognition as sr
import time
import os
import webbrowser
import requests

def Str2MinusStr1 (str1, str2, n=1):
    # Copied From https://stackoverflow.com/questions/18454570/how-can-i-subtract-two-strings-in-python
    return sub(r'%s' % (str2), '', str1, n)

def speak(audio):
    tts = gTTS(text=audio, lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")

def wishme():
    current_hour = int(datetime.now().hour)
    if current_hour < 12:
        speak("Hello! Good Morning Sir.")
    elif current_hour > 12 and current_hour < 5:
        speak("Hello! Good After Noon Sir.")
    elif current_hour > 19:
        speak("Hello! Good Night Sir.")
    else:
        speak("Hello! Good Evening Sir.")

def take_input():
    mic = "default"
    r = sr.Recognizer() 

    mic_list = sr.Microphone.list_microphone_names()

    for i, microphone_name in enumerate(mic_list): 
        if microphone_name == mic: 
            device_id = i
    
    with sr.Microphone(device_index = device_id) as source: 
        
        # r.adjust_for_ambient_noise(source) 
        print ("Listening")
        r.pause_threshold = 1
        audio = r.listen(source) 
            
        try: 
            text = r.recognize_google(audio,language='en-in')
            print ("you said: " + text)
            # do_task(text)+
             
        except sr.UnknownValueError: 
            print("Google Speech Recognition could not understand audio") 
        
        except sr.RequestError : 
            print("Could not request results from Google")


def open_google():
    webbrowser.open("http://www.google.com")

def open_youtube():
    webbrowser.open("http://www.youtube.com")

def search_google(word):

    url = 'https://www.google.com/search'
    playloads = {"q":word}

    req = requests.get(url, params=playloads)
    soup = BeautifulSoup(req.text,'html.parser')

    First_website = soup.find('cite').text
    speak("Here are some matching Result")
    webbrowser.open(First_website)

def search_youtube(word):
    url = 'https://www.youtube.com/results'
    playloads = {"search_query":word}

    req = requests.get(url, params=playloads)
    soup = BeautifulSoup(req.text,'html.parser')

    First_video = soup.find('a',class_='yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link')

    First_video_link = 'http://youtube.com' + First_video.get("href")

    webbrowser.open(First_video_link)

def wikiHowSearch(word):
    url = 'https://wikihow.com/wikiHowTo'
    playloads = {'search':word}
    req = requests.get(url, params=playloads)
    soup = BeautifulSoup(req.text,'html.parser')

    First_link = soup.find('a',class_='result_link')

    url = First_link['href']
    req = requests.get(url)
    soup = BeautifulSoup(req.text,'html.parser')
    parts = soup.find_all('span',class_='mw-headline')[:-6]
    steps = soup.find_all('div',class_='step')

    speak(f"It was Divided in {len(parts)} parts ")
    webbrowser.open(url)

    for i in parts:
        speak(i.text)
    
    for i in steps:
        speak(i.text)

def weathernow():
    url = 'https://www.bbc.com/weather/1261481'
    req = requests.get(url)
    soup = BeautifulSoup(req.text,'html.parser')

    TempInText = soup.find('div',class_='wr-day__weather-type-description wr-js-day-content-weather-type-description wr-day__content__weather-type-description--opaque').text
    
    temp = soup.find_all('span',class_='wr-value--temperature--c')[:2]

    speak(f"Todays temperature is {TempInText}. Minimum temperature {temp[0].text } and Maximum temperature is {temp[1].text }")

def date_time():
    print(str(datetime.now())[:-7])

def set_timer(seconds):
    current_time = time.time()
    timer_time = current_time + seconds

    print("Start")
    while time.time() != timer_time:
        if time.time() == timer_time:
            os.system('mpg321 alarm.mp3')

def caluclate(equation):
    print(eval(equation))

def aboutyou():
    speak("I am a Program which can automate your task created by Nikhil Raj Pandey.")

def do_task(task):
    if 'open google' in task:
        open_google()

    elif 'open youtube' in task:
        open_youtube()

    elif 'search google' in task:
        Str2MinusStr1('task','search google')
        search_google(task)

    elif 'play' in task:
        Str2MinusStr1('task','play')
        search_youtube(task)

    elif 'search wikihow' in task:
        Str2MinusStr1(task,'search wikihow')
        wikiHowSearch(task)

    elif 'weather now' in task:
         weathernow()

    elif 'calculate' in task:
        Str2MinusStr1(task,'calculate')
        caluclate(task)

    elif 'set timer' in task:
        Str2MinusStr1(task,'set timer')
        set_timer(task)

    elif 'time now' in task:
        date_time()
    
    elif 'about you' in task:
        aboutyou()
wishme()

while True:
    take_input()



