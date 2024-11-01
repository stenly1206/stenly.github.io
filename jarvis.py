import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import sys
import socket
import requests
import webbrowser

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


# Mendapatkan nama komputer
def get_computer_name():
    return socket.gethostname()

nama_komputer = get_computer_name()

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = r.listen(source, timeout=30, phrase_time_limit=30)
        except sr.WaitTimeoutError:
            standby_command()
            return "None"
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"{nama_komputer}: {query}\n")
    except Exception as e:
        speak("Say that again please...")
        return "None"
    return query

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        speak("Good morning Stenly")
    elif hour > 12 and hour < 18:
        speak("Good afternoon Stenly")
    else:
        speak("Good evening Stenly")
    speak("Welcome to the Jarvis Assistant service. How can I help you?")

def standby_command():
    while True:
        query = takecommand().lower()
        if "jarvis" in query:
            speak("Yes, I'm here. How can I assist you?")
            main()
            break
        elif "no" in query:
            username = os.getenv('USERNAME')
            speak(f"Alright, have a good day {username}!")
            sys.exit()
        else:
            speak("I'm on standby mode. Say 'Jarvis' to wake me up.")

def main():
    while True:
        query = takecommand().lower()

        if "standby" in query:
            print("STATUS: Entering standby mode...")
            speak("Standby mode activated. Say 'Jarvis' to wake me up.")
            standby_command()

        elif "open exam" in query:
            xpath = "C:\\xampp\\xampp-control.exe"
            os.startfile(xpath)

        elif "open command prompt" in query:
            os.system("start cmd")

        elif "open file explorer" in query:
            folder_path = "D:\\"
            os.startfile(folder_path)

        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('Webcam', img)
                k = cv2.waitKey(1) & 0xff
                if k == 27 or k == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    break

        elif "nothing" in query:
            speak("Goodbye Stenly, thank you for using Assistant Jarvis. See you next time!")
            sys.exit()

        elif "hi jarvis do you know me" in query:
            speak("Yes, you are Stenly, one of the students at Universitas Pamulang Kampus 2 (UNPAM Viktor) semester 5.")

        elif "where is my university location" in query:
            speak("Universitas Pamulang Kampus 2 (UNPAM Viktor) is located on Jl. Raya Puspitek, Buaran, Kec. Pamulang, Kota Tangerang Selatan, Banten 15310")
            webbrowser.open("https://www.google.com/maps/place/Universitas+Pamulang+Kampus+2+(UNPAM+Viktor)")

        elif "my ip address" in query:
            ip = requests.get('https://api.ipify.org').text
            speak(f"Your IP Address is {ip}")

        elif "open google" in query:
            webbrowser.get().open("https://www.google.com/")
            speak("What would you like to search for?")
            recognizer = sr.Recognizer()

            with sr.Microphone() as source:
                audio = recognizer.listen(source)

            try:
                query = recognizer.recognize_google(audio)
                print(f"You searched for: {query}")
                search_url = f"https://www.google.com/search?q={'+'.join(query.split())}"
                webbrowser.get().open(search_url)
            except sr.UnknownValueError:
                speak("Sorry, I couldn't recognize your voice.")
            except sr.RequestError as e:
                speak(f"Error processing request: {e}")

        elif "open maps" in query:
            webbrowser.get().open("https://www.google.com/maps")
            speak("What location would you like to search for?")
            recognizer = sr.Recognizer()

            with sr.Microphone() as source:
                audio = recognizer.listen(source)

            try:
                query = recognizer.recognize_google(audio)
                print(f"You searched for location: {query}")
                search_url = f"https://www.google.com/maps/search/?api=1&query={'+'.join(query.split())}"
                webbrowser.get().open(search_url)
            except sr.UnknownValueError:
                speak("Sorry, I couldn't recognize your voice.")
            except sr.RequestError as e:
                speak(f"Error processing request: {e}")

        elif "open youtube" in query:
            webbrowser.get().open("http://www.youtube.com")
            speak("What video would you like to search for?")
            recognizer = sr.Recognizer()

            with sr.Microphone() as source:
                audio = recognizer.listen(source)

            try:
                query = recognizer.recognize_google(audio)
                print(f"You searched for: {query}")
                search_url = f"http://www.youtube.com/results?search_query={'+'.join(query.split())}"
                webbrowser.get().open(search_url)
            except sr.UnknownValueError:
                speak("Sorry, I couldn't recognize your voice.")
            except sr.RequestError as e:
                speak(f"Error processing request: {e}")

        else:
            speak("I don't understand your command.")
        
        print("")
        speak("Do you have any other requests, Stenly?")

if __name__ == "__main__":
    wish()
    main()