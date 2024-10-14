import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import datetime
import subprocess
import time
import requests
import smtplib
import random
import ctypes
from googletrans import Translator
from datetime import datetime, timedelta
import winsound

# Initialize the recognizer and the engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def set_voice():
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'english' in voice.languages and 'male' in voice.name.lower() and 'uk' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break

# Set the voice to a British male voice
set_voice()

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to take the command from the user
def take_command():
    try:
        with sr.Microphone() as source:
            print("Waiting for your command sir...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}\n")
            return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not get that sir")
        return "None"
    except sr.RequestError:
        speak("Sorry, my speech service is down")
        return "None"

# Function to get the news headlines
def get_news():
    speak("Fetching the latest news headlines sir")
    url = 'https://newsapi.org/v2/top-headlines?country=za&apiKey=abf7b1312b224ccb8028b84db9a89b8c'
    response = requests.get(url)
    news_data = response.json()
    articles = news_data['articles'][:5]
    for i, article in enumerate(articles):
        speak(f"The top news of the day is: {i + 1}: {article['title']} sir")

# Reminders list
reminders = []

# Function to set reminder
def set_reminder(reminder, seconds):
    reminders.append((reminder, time.time() + seconds))
    speak(f"Reminder set for {reminder} in {seconds // 60} minutes sir")

# Function to check reminders
def check_reminders():
    current_time = time.time()
    for reminder, remind_time in reminders:
        if current_time >= remind_time:
            speak(f"Reminder: {reminder} sir")
            reminders.remove((reminder, remind_time))

# Function to send email
def send_email(to, subject, body):
    speak("Sending email sir")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your_email@gmail.com', 'your_password')
    message = f'Subject: {subject}\n\n{body}'
    server.sendmail('your_email@gmail.com', to, message)
    server.quit()
    speak("Email sent sir")

# Function to give daily affirmation
def daily_affirmation():
    affirmations = [
        "You are doing a great job, keep it up!",
        "Believe in yourself, you have the power to achieve great things!",
        "Stay positive and good things will happen.",
        "You are capable of amazing things.",
        "Every day is a new opportunity to grow and be better."
    ]
    affirmation = random.choice(affirmations)
    speak(affirmation)

def joke():
    jokes = [
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "What do you call fake spaghetti? An impasta!",
        "Why don’t scientists trust atoms? Because they make up everything!",
        "How does a penguin build its house? Igloos it together!",
        "Why did the golfer bring two pairs of pants? In case he got a hole in one!",
        "What do you call cheese that isn't yours? Nacho cheese!",
        "Why did the math book look sad? Because it had too many problems.",
        "What do you call a bear with no teeth? A gummy bear!",
        "Why don't skeletons fight each other? They don't have the guts.",
        "What do you call a fish wearing a bowtie? Sofishticated!"
    ]
    joke = random.choice(jokes)
    speak(joke)

# Function to provide a motivational quote
def motivational_quote():
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "The harder you work for something, the greater you'll feel when you achieve it.",
        "Dream bigger. Do bigger.",
        "Don’t stop when you’re tired. Stop when you’re done.",
        "Wake up with determination. Go to bed with satisfaction."
    ]
    quote = random.choice(quotes)
    speak(quote)

# Function to translate text
def translate_text(text, dest_lang='es'):
    translator = Translator()
    translation = translator.translate(text, dest=dest_lang)
    speak(f"The translation is: {translation.text}")

# Function to set volume
def set_volume(volume):
    devices = ctypes.windll.winmm.waveOutGetNumDevs()
    ctypes.windll.winmm.waveOutSetVolume(0, int(volume * 65535 / 100))
    speak(f"Volume set to {volume} percent sir")

#Function to set an alarm
def set_alarm(alarm_time):
    # Ensure alarm_time is in HH:MM format
    if len(alarm_time) == 4 and alarm_time.isdigit():
        alarm_time = f"{alarm_time[:2]}:{alarm_time[2:]}"
    
    speak(f"Alarm set for {alarm_time}")
    
    while True:
        current_time = datetime.now().strftime("%H:%M")
        if current_time == alarm_time:
            speak("Alarm ringing!")
            winsound.Beep(1000, 10000)  # Beep sound
            break

# Function to handle Google search queries
def google_search(search_query):
    base_url = "https://www.google.com/search?q="
    webbrowser.open(base_url + search_query.replace(" ", "+"))  # Replace spaces in the query with '+'
    speak(f"Here are the search results for {search_query} sir")

#THE CODE FOR THE GOOLGE FUNCTION IN ORDER TO ACTIVELY VOICE SEARCH
def open_google():
    speak("Opening Google, sir. What would you like to search for?")
    
    while True:
        search_query = take_command()  # Capture the follow-up command (search query)

        # Exit the search
        if "stop search" in search_query:
            speak("Closing Google, sir.")
            subprocess.call(["taskkill", "/IM", "chrome.exe", "/F"])
            break

        # Clear the search and prompt for a new search
        elif "clear search" in search_query:
            speak("What would you like to search for next, sir?")
            continue  # Continue the loop to capture a new search query
        
        # Perform Google search for the given query
        elif search_query != "None":
            google_search(search_query)  # Perform Google search


# Function to execute commands
def execute_command(command):

    #Adding in new commands to expand HUSTLEBOT
    if 'open google' in command:
        open_google()  # Call the function to open Google and manage searches
    elif 'close google' in command:
        speak("Closing Google, sir.")
        subprocess.call(["taskkill", "/IM", "chrome.exe", "/F"])
    else:
        speak("Sorry, I don't know that command, sir.")

    if 'open youtube' in command:
        speak("Opening YouTube sir")
        webbrowser.open("https://www.youtube.com")
    elif 'close youtube' in command:
        speak("Closing YouTube sir")
        subprocess.call(["taskkill", "/IM", "chrome.exe", "/F"])
    elif 'open brave' in command:
        speak("Opening Brave sir")
        webbrowser.open("Brave.exe")
    elif 'close Brave' in command:
        speak("Closing Brave sir")
        subprocess.call(["taskkill", "/IM", "Brave.exe", "/F"])
    elif 'weather today' in command:
        speak("Checking the weather for today sir")
        webbrowser.open("https://www.accuweather.com/en/za/pretoria/305449/daily-weather-forecast/305449")
    elif 'thank you for the weather' in command:
        speak("You're welcome sir, have a lovely day")
        subprocess.call(["taskkill", "/IM", "chrome.exe", "/F"])
    elif 'the time' in command:
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is currently {str_time} - Next time carry a watch with you sir")
    elif 'open facebook' in command:
        speak("Opening Facebook sir")
        webbrowser.open("https://www.facebook.com")
    elif 'close facebook' in command:
        speak("Closing Facebook sir")
        subprocess.call(["taskkill", "/IM", "chrome.exe", "/F"])
    elif 'open university' in command:
        speak("Opening your university website sir")
        webbrowser.open("https://www.varsitycollege.co.za/")
    elif 'close university' in command:
        speak("Closing university website sir")
        subprocess.call(["taskkill", "/IM", "chrome.exe", "/F"])
    elif 'open student portal' in command:
        speak("Opening your student portal sir")
        webbrowser.open("https://student.varsitycollege.co.za/student-portal/#/login")
    elif 'close student portal' in command:
        speak("Closing student portal sir")
        subprocess.call(["taskkill", "/IM", "chrome.exe", "/F"])
    elif 'open gmail' in command:
        speak("Opening Gmail - you have plenty new emails waiting for you")
        webbrowser.open("https://mail.google.com/mail/u/0/?ogbl#inbox")
    elif 'close gmail' in command:
        speak("Closing Gmail")
        subprocess.call(["taskkill", "/IM", "chrome.exe", "/F"])
    elif 'open chat' in command:
        speak("Opening ChatGPT sir")
        webbrowser.open("https://chat.openai.com/")
    elif 'close chat' in command:
        speak("Closing ChatGPT sir")
        subprocess.call(["taskkill", "/IM", "chrome.exe", "/F"])
    elif 'play music' in command:
        music_dir = 'C:\\Users\\YourUsername\\Music'  # Update the path to your music directory
        songs = os.listdir(music_dir)
        os.startfile(os.path.join(music_dir, songs[0]))
    elif 'stop music' in command:
        speak("Stopping music sir")
        subprocess.call(["taskkill", "/IM", "wmplayer.exe", "/F"])
    elif 'open settings' in command:
        speak("Opening Settings menu sir")
        subprocess.Popen(['start', 'ms-settings:'], shell=True)
    elif 'close settings' in command:
        speak("Closing Settings menu sir")
        subprocess.call(["taskkill", "/IM", "SystemSettings.exe", "/F"])
    elif 'open calculator' in command:
        speak("Opening Calculator sir")
        subprocess.Popen('calc.exe')
    elif 'close calculator' in command:
        speak("Closing Calculator sir")
        subprocess.call(["taskkill", "/IM", "calculator.exe", "/F"])
    elif 'tell me a joke' in command:
        joke = "Why don't scientists trust atoms? Because they make up everything!"
        speak(joke)
    elif 'open file explorer' in command:
        speak("Opening File Explorer sir")
        subprocess.Popen('explorer.exe')
    elif 'create new folder' in command:
        speak("Creating a new folder on your Desktop sir")
        os.makedirs(os.path.join(os.path.expanduser("~/Desktop"), "New Folder"), exist_ok=True)
    elif 'news' in command:
        get_news()
    elif 'set a reminder' in command:
        speak("What should I remind you about sir?")
        reminder = take_command()
        speak("In how many minutes?")
        minutes = int(take_command())
        set_reminder(reminder, minutes * 60)
    elif 'send an email' in command:
        speak("To whom should I send the email sir?")
        to = take_command()
        speak("What is the subject sir?")
        subject = take_command()
    elif 'open new document' in command:
        speak("Opening a new Word document sir")
        subprocess.Popen('winword.exe')
    elif 'close document' in command:
        speak("Closing your Word document sir")
        subprocess.call(["taskkill", "/IM", "winword.exe", "/F"])
    elif 'open spreadsheet' in command:
        speak("Opening a new Excel spreadsheet sir")
        subprocess.Popen('excel.exe')
    elif 'close spreadsheet' in command:
        speak("Closing your Excel spreadsheet sir")
        subprocess.call(["taskkill", "/IM", "excel.exe", "/F"])
    elif 'open Notion' in command:
        speak("Opening Notion sir")
        subprocess.Popen(["start", "notion"], shell=True)
    elif 'close Notion' in command:
        speak("Closing Notion sir")
        subprocess.call(["taskkill", "/IM", "notion.exe", "/F"])

    #Setting an alarm
    elif 'set an alarm' in command:
        speak("What time should I set the alarm for? Please use HH:MM format.")
        alarm_time = take_command()
        set_alarm(alarm_time)
        return "exit"

    #Coding commands
    elif 'open code' in command:
        speak("Opening Visual Studio Code sir")
        subprocess.Popen(["code"])
    elif 'Closing Visual Studio Code sir' in command:
        speak("Close Code")
        subprocess.call(["taskkill", "/IM", "Code.exe", "/F"])
    elif 'open terminal' in command:
        speak("Opening Hyper sir")
        subprocess.Popen(['hyper'])
   
    #Exiting the code
    elif 'we are done for today' in command:
        speak("Goodbye! I'll be waiting to hear from you soon.")
        return "exit"  # Signal to exit the current session
    else:
        speak("Sorry, I don't know that command sir")


# Main function to run the assistant
def hustle():
    speak("Hello, I am Hustle. How can I assist you today?")
    while True:
        command = take_command()
        if command != "None":
            execute_command(command)
        if 'we are done for today' in command or 'stop' in command:
            speak("Goodbye")
            break

# Function to continuously listen for the keyword "Hustle"
def listen_for_hustle():
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for 'Hustle'...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                keyword = recognizer.recognize_google(audio)
                if "hustle" in keyword.lower():
                    hustle()
        except sr.UnknownValueError:
            continue
        except sr.RequestError:
            speak("Sorry sir, it appears my speech service is down")
            break

if __name__ == "__main__":
    listen_for_hustle()
