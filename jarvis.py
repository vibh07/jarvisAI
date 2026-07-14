"""
Jarvis Voice Assistant - natural, ChatGPT/Gemini-style conversation, powered by
Google Gemini's FREE API tier (no credit card, no payment needed).

SETUP REQUIRED before running:
1. pip install google-genai python-decouple SpeechRecognition pyttsx3 pywhatkit wikipedia requests pypiwin32
2. Get a free Gemini API key: go to https://aistudio.google.com/app/apikey,
   sign in with any Google account, click "Create API key". No card needed.
3. Create a file named ".env" in the same folder as this script with:
       GEMINI_API_KEY=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
       NEWS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxx   (optional, only needed for the "news" command)
4. Run: python jarvis.py
"""

import datetime
import re
import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import subprocess as sp
import requests
import pywhatkit as kit
from decouple import config
from google import genai
from google.genai import types
from pprint import pprint

# ------------------------------------------------------------------
# TEXT TO SPEECH SETUP
# ------------------------------------------------------------------
VOICE_INDEX = 0  # voice[0] = usually a male voice, voice[1] = usually female (Windows default)

# ------------------------------------------------------------------
# GEMINI SETUP (FREE tier) -> yahi cheez ab Jarvis ko ChatGPT/Gemini
# jaisa natural, conversational bana degi -- bina ek rupaya kharch kiye
# ------------------------------------------------------------------
gemini_client = genai.Client(api_key=config("GEMINI_API_KEY"))

# Chat session khud conversation memory maintain karta hai -- isi se
# follow-up sawaal bhi context ke saath samajh mein aate hain, bilkul
# ChatGPT/Gemini voice mode ki tarah
chat_session = gemini_client.chats.create(
    model="gemini-3.5-flash",  # current free-tier model, generous daily limit
    config=types.GenerateContentConfig(
        system_instruction=(
            "You are Jarvis, a warm and witty voice assistant speaking to your user "
            "out loud. Keep every reply short -- 1 to 3 sentences -- natural and "
            "conversational, since a text-to-speech engine will read it aloud. "
            "Never use markdown, bullet points, asterisks, or emojis, since those "
            "cannot be spoken. If you don't know the answer, say so honestly."
        ),
        thinking_config=types.ThinkingConfig(thinking_level=types.ThinkingLevel.LOW),
    )
)


def ask_jarvis(user_text):
    """
    User ki baat Gemini ko bhejta hai -- chat_session khud history sambhalta
    hai, isliye natural back-and-forth baatcheet possible hoti hai.

    Response STREAM mein aata hai aur jaise hi ek poora sentence ban jaata hai,
    Jarvis turant usse bolna shuru kar deta hai (baaki text peeche generate
    hota rehta hai) -- isse poore jawab ka wait nahi karna padta, delay bahut
    kam mehsoos hota hai, bilkul ChatGPT/Gemini voice mode ki tarah.
    Print aur speak dono yahin ho jaate hain, isliye har jawab guaranteed
    bola bhi jaata hai, sirf text nahi rehta.
    """
    buffer = ""
    try:
        for chunk in chat_session.send_message_stream(user_text):
            if not chunk.text:
                continue
            buffer += chunk.text

            # jaise hi ek complete sentence mil jaaye, turant bol do
            while True:
                match = re.search(r'[.!?](\s|$)', buffer)
                if not match:
                    break
                sentence = buffer[:match.end()].strip()
                buffer = buffer[match.end():]
                if sentence:
                    print(f"Jarvis: {sentence}")
                    speak(sentence)

        leftover = buffer.strip()
        if leftover:
            print(f"Jarvis: {leftover}")
            speak(leftover)

    except Exception as e:
        print(f"Gemini error: {e}")
        error_msg = "Sorry sir, I couldn't reach my brain right now. Please check the API key or your internet."
        print(f"Jarvis: {error_msg}")
        speak(error_msg)


def takeCommand():
    """
    Microphone se voice input leta hai aur usse text mein convert karke return karta hai.
    """
    r = sr.Recognizer()
    with sr.Microphone(0) as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception:
        print("Sorry, didn't catch that. Please say it again...")
        return "None"
    return query


def speak(audio):
    """
    Har call pe fresh engine banate hain -- SAPI5 mein known issue hai ki
    same engine instance se baar-baar bolne pe (jaise streaming mein
    multiple sentences) awaaz silently band ho jaati hai, sirf text reh
    jaata hai. Naya engine har baar reliably bolta hai.
    """
    tts_engine = pyttsx3.init('sapi5')
    tts_voices = tts_engine.getProperty('voices')
    tts_engine.setProperty('voice', tts_voices[VOICE_INDEX].id)
    tts_engine.setProperty('rate', 175)
    tts_engine.say(audio)
    tts_engine.runAndWait()
    tts_engine.stop()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am jarvis sir. Please tell me how may i help you")


def search_on_google(query):
    kit.search(query)


def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)


def open_notepad():
    path = "C:\\Program Files\\Notepad++\\notepad++.exe"
    os.startfile(path)


def open_cmd():
    os.system('start cmd')


def open_calculator():
    sp.Popen(paths['calculator'])


def send_whatsapp_message(number, message):
    kit.sendwhatmsg_instantly(f"+91{number}", message)


def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]


def get_latest_news():
    NEWS_API_KEY = config("NEWS_API_KEY")  # bug fix: pehle yahan actual key string hardcoded thi
    news_headlines = []
    res = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}&category=general").json()
    articles = res["articles"]
    for article in articles:
        news_headlines.append(article["title"])
    return news_headlines[:5]


def get_random_joke():
    headers = {'Accept': 'application/json'}
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]


def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']


# ------------------------------------------------------------------
# MAIN LOOP -> continuous, hands-free chalega (jaise ChatGPT/Gemini
# voice mode) -- koi menu ya keypress nahi, bas bolte raho
# ------------------------------------------------------------------
if __name__ == "__main__":

    paths = {
        'notepad': "C:\\Program Files\\Notepad++\\notepad++.exe",
        'calculator': "C:\\Windows\\System32\\calc.exe"
    }

    speak("Hi sir")
    wishMe()
    print("\nJarvis is listening continuously. Say 'stop listening' anytime to exit.\n")

    EXIT_PHRASES = ['stop listening', 'goodbye jarvis', 'exit jarvis', 'quit jarvis', 'bye jarvis']

    while True:
        query = takeCommand().lower()

        if query == "none" or query.strip() == "":
            continue

        if any(phrase in query for phrase in EXIT_PHRASES):
            speak("Goodbye sir, talk to you soon!")
            break

        # ---------------- FAST, INSTANT COMMANDS (no API call needed) ----------------

        if query.startswith("open "):
            application = query.replace("open ", "").strip()
            speak(f"Opening {application}")

            if 'youtube' in query:
                webbrowser.open("youtube.com")
            elif 'google' in query:
                webbrowser.open("google.com")
            elif 'stackover' in query:
                webbrowser.open("stackoverflow.com")
            elif 'notepad' in query:
                open_notepad()
            elif 'command prompt' in query or 'cmd' in query:
                open_cmd()
            elif 'camera' in query:
                open_camera()
            elif 'calculator' in query:
                open_calculator()
            elif 'code' in query:
                codePath = "C:\\Users\\Lenovo\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                os.startfile(codePath)
            elif 'game' in query:
                gamePath = "C:\\Users\\Lenovo\\Downloads\\Grand Theft Auto Vice City Full Version\\gta-vc.exe"
                os.startfile(gamePath)
            else:
                speak("Sorry sir, I don't know how to open this application yet.")

        elif 'play music' in query:
            music_dir = 'D:\\Non Critical\\songs\\Favorite Song2'
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
            else:
                speak("No songs found in the directory, sir.")

        elif 'the time' in query:
            strTime = str(datetime.datetime.now().strftime("%H:%M:%S"))
            print(f"sir, the time is {strTime}")
            speak(f"sir, the time is {strTime}")

        elif "send whatsapp message" in query:
            speak('On what number should I send the message, sir?')
            number = takeCommand()
            speak("What is the message, sir?")
            message = takeCommand()
            send_whatsapp_message(number, message)
            speak("I've sent the message sir.")

        elif 'search on google' in query or 'google search' in query:
            speak('What do you want to search on Google, sir?')
            search_query = takeCommand()
            search_on_google(search_query)

        elif 'joke' in query:
            speak("Hope you like this one sir")
            joke = get_random_joke()
            speak(joke)
            pprint(joke)

        elif "advice" in query:
            speak("Here's an advice for you, sir")
            advice = get_random_advice()
            speak(advice)
            pprint(advice)

        elif 'news' in query:
            speak("I'm reading out the latest news headlines, sir")
            headlines = get_latest_news()
            for h in headlines:
                speak(h)
            print(*headlines, sep='\n')

        elif 'wikipedia' in query:
            speak('Searching Wikipedia...')
            wiki_query = query.replace("wikipedia", "").strip()
            try:
                results = wikipedia.summary(wiki_query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception:
                speak("Sorry sir, I couldn't find anything relevant on Wikipedia.")

        # ---------------- EVERYTHING ELSE -> NATURAL CONVERSATION VIA GEMINI ----------------

        else:
            ask_jarvis(query)
