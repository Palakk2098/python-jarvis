import speech_recognition as sr
import webbrowser
import pyttsx3
import sounddevice
import musicLibrary
import requests
import pygame
import os
from openai import OpenAI
from gtts import gTTS

recognizer=sr.Recognizer()
engine=pyttsx3.init()


# sounddevice installation and imports solved problems related to alsa 
def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")

    pygame.mixer.init()

    pygame.mixer.music.load("temp.mp3")

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def aiProcess(command):
    client = OpenAI(
        api_key="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"
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Give short responses."},
            {
                "role": "user",
                "content": command
            }
        ]
    )
    return completion.choices[0].message.content

def processCommand(cmd):
    
    if "open google" in cmd.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in cmd.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in cmd.lower():
        webbrowser.open("https://youtube.com")
    elif "open linked in" in cmd.lower():
        webbrowser.open("https://linkedin.com")
    elif "play" in cmd.lower():
        music=cmd.split(" ")[1]
        song=musicLibrary[music]
        webbrowser.open(song)
    elif "news" in cmd.lower():
        data=requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey=66b60524529749de8aa0fa90f5590ac1")
        
        data=data.json()
        if(data.status==200):
            news = [item["title"] for item in data["articles"]]

            for i in range(1,len(news)):
                speak(i)
    else:
        # Open AI handling
        output=aiProcess(cmd)
        speak(output)

        

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        try:
            # Obtain audio from the microphone
            r = sr.Recognizer()
    
            with sr.Microphone() as source:
                print("Listening!")
                
                audio = r.listen(source,timeout=2,phrase_time_limit=1)
                # Recognize speech using Google
                print("Recognizing!")
               
                word= r.recognize_google(audio)
                print(word,"word")
                
                if(word.lower()=="jarvis"):
                        speak("Ya")
                        print(word.lower(),"word")
                        # Listen for command
                        with sr.Microphone() as source:
                            print("Jarvis Active...")
                            audio = r.listen(source)

                            # Recognize speech using Google
                            print("Jarvis Recognizing!")
                            command= r.recognize_google(audio)
                            processCommand(command)        

                
                # print("Google thinks you said " + r.recognize_google(audio))

        except Exception as e:
            print("Error; {0}".format(e))