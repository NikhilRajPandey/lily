from bs4 import BeautifulSoup
from gtts import gTTS
from datetime import datetime
import speech_recognition as sr
import time
import os
import webbrowser
import requests

def speak(audio):
    tts = gTTS(text=audio, lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")

def wishme():
    speak("Hello! Good After Noon Sir.")

def take_input():
    mic = "default"
    r = sr.Recognizer() 

    mic_list = sr.Microphone.list_microphone_names()

    for i, microphone_name in enumerate(mic_list): 
        if microphone_name == mic: 
            device_id = i
    
    with sr.Microphone(device_index = device_id) as source: 
        
        r.adjust_for_ambient_noise(source) 
        print ("Listening")
        
        audio = r.listen(source) 
            
        try: 
            text = r.recognize_google(audio) 
            print ("you said: " + text) 
        
        
        except sr.UnknownValueError: 
            print("Google Speech Recognition could not understand audio") 
        
        except sr.RequestError : 
            print("Could not request results from Google")

    return text

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
            break

wishme()
speak("The program is in Devlopment when it will ready then it will take voice command")
