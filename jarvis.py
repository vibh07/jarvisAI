import datetime
import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import subprocess as sp
import requests
import pywhatkit as kit
from email.message import EmailMessage
import sched
from decouple import config
import requests
from pprint import pprint


engine = pyttsx3.init('sapi5') 
voices = engine.getProperty('voices')
print(voices[1].id)
engine.setProperty('voice',voices[0].id)

def takeCommand():

    # It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone(0) as source:
        speak("i am listening sir!")
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in') #Using google for voice recognition.
        print(f"User said: {query}\n")  #User query will be printed.

    except Exception as e:
        # print(e)    
        print("Say that again please...")   #Say that again will be printed in case of improper voice 
        return "None" #None string will be returned
    return query

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
               

def takeCommands():
    '''
    It takes user's voice as input
    '''
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio=r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"Recognized Command: {query}")

    except Exception as e:
        print(e)
        print("I didn't recognize what you said please repeat")
        return "None"

    return query

def speak(audio   ):  #, Ticon
    # if  Ticon == 1:
        engine.say(audio)
        engine.runAndWait()
        
  

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

        speak("I am jarvis sir . Please tell me how may i help you")

def search_on_google(query):
    kit.search(query) 

def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)

def open_notepad():
    # os.startfile("C:\\program Files\\WindowsApp\\Microsoft.WindowsNotepad_11.2210.5.0_x64__8wekyb3d8bbwe\\Notepad\\Notepad.exe")
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

 #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#  TMDB_API_KEY = config("TMDB_API_KEY")  


# def get_trending_movies():
#     trending_movies = []
#     res = requests.get(
#         f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}").json()
#     results = res["results"]
#     for r in results:
#         trending_movies.append(r["original_title"])
#     return trending_movies[:5]

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def get_latest_news():
    NEWS_API_KEY = config("a106524326d44ba483caedc576a60dce")
    news_headlines = []
    res = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}&category=general").json()
    articles = res["articles"]
    for article in articles:
        news_headlines.append(article["title"])
    return news_headlines[:5]

def get_random_joke():
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]

def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']



  #///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////







# OPENWEATHER_APP_ID = config("OPENWEATHER_APP_ID")  
# def get_weather_report(city):
#     res = requests.get(
#         f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_APP_ID}&units=metric").json()
#     weather = res["weather"][0]["main"]
#     temperature = res["main"]["temp"]
#     feels_like = res["main"]["feels_like"]
#     return weather, f"{temperature}℃", f"{feels_like}℃"






# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

if __name__ == "__main__":
    speak(" hi sir")
    wishMe()
    while True:
        co = input("Enter 1 for voice.\nEnter any key for text\n Enter option :")

        if co == "1":
            query = takeCommand().lower() #Converting user query into lower case
        else:
            query = input("Enter searched text. -->")

        # Logic for executing tasks based on query

        # if 'wikipedia' in query:  #if wikipedia found in the query then this block will be executed
        #     speak('Searching Wikipedia...')
        #     query = query.replace("wikipedia", "")
        #     results = wikipedia.summary(query, sentences=2) 
        #     speak("According to Wikipedia")
        #     print(results)
        #     speak(results)

        try:

            if (query.index("open ") == 0):
                lst = query.split()
                application = lst[1]
                speak("user is trying to open" + application)
                
        
        except:
       
            if 'open youtube' in query:
                webbrowser.open("youtube.com")
    
            elif 'open google' in query:
                webbrowser.open("google.com")

            elif 'open stackover' in query:
                webbrowser.open("stackoverflow.com")
            
            elif 'open notepad' in query:
                open_notepad()


            elif 'open command prompt' in query or 'open cmd' in query:
                open_cmd()

            elif 'open camera' in query:
                open_camera()

            elif 'open calculator' in query:
                open_calculator()

            elif 'play music' in query:
                music_dir = 'D:\\Non Critical\\songs\\Favorite Song2'               
                songs = os.listdir(music_dir)
                print(songs)
                os.startfile(os.path.join(music_dir, songs[0]))

            elif 'the time' in query:
                strTime = str(datetime.datetime.now().strftime("%H:%M:%S"))
                print(f"sir, the time is {strTime}")
                speak(f"sir, the time is {strTime}") 
                # pprint( strTime)
                
                

            elif "send whatsapp message" in query:
                speak('On what number should I send the message sir? Please enter in the console: ')
                number = input("Enter the number: ")
                speak("What is the message sir?")
                message = input("Enter the message: ")
                send_whatsapp_message(number, message)
                speak("I've sent the message sir.")

            
            elif 'from google' in query:
                speak('What do you want to search on Google, sir?')
                query = input("Enter the query: ")
                search_on_google(query)

            
            elif 'joke' in query:
                speak(f"Hope you like this one sir")
                joke = get_random_joke()
                speak(joke)
                speak("For your convenience, I am printing it on the screen sir.")
                pprint(joke)

            elif "advice" in query:
                speak(f"Here's an advice for you, sir")
                advice = get_random_advice()
                speak(advice)
                speak("For your convenience, I am printing it on the screen sir.")
                pprint(advice)



            # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

            
            # elif "trending movies" in query:
            #     speak(f"Some of the trending movies are: {get_trending_movies()}")
            #     speak("For your convenience, I am printing it on the screen sir.")
            #     print(*get_trending_movies(), sep='\n')

            # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

            elif 'news' in query:
                speak(f"I'm reading out the latest news headlines, sir")
                speak(get_latest_news())
                speak("For your convenience, I am printing it on the screen sir.")
                print(*get_latest_news(), sep='\n')

            # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

            # elif 'weather' in query:
            #     ip_address = find_my_ip()
            #     city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            #     speak(f"Getting weather report for your city {city}")
            #     weather, temperature, feels_like = get_weather_report(city)
            #     speak(f"The current temperature is {temperature}, but it feels like {feels_like}")
            #     speak(f"Also, the weather report talks about {weather}")
            #     speak("For your convenience, I am printing it on the screen sir.")
            #     print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")




            # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



            elif 'open code' in query:
                codePath = "C:\\Users\\Lenovo\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                os.startfile(codePath)

            elif 'open game' in query:
                gamePath = "C:\\Users\\Lenovo\\Downloads\\Grand Theft Auto Vice City Full Version\\gta-vc.exe"
                os.startfile(gamePath)
                paths = {'notepad': "C:\\Program Files\\Notepad++\\notepad++.exe",
                'calculator': "C:\\Windows\\System32\\calc.exe"}

            else:  #if wikipedia found in the query then this block will be executed
                speak('Searching ${query} in Wikipedia...')
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2) 
                speak("According to Wikipedia")
                print(results)
                speak(results)

            # else:
            #     speak("I am not answerable to this quistions?")
            #     speak('I feel better Thank you for it')



    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////





