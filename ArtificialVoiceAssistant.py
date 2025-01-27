import speech_recognition as sr
import pyttsx3
import requests
import json
import datetime
import wikipedia

# Initialize the recognizer and the text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return ""

def get_weather(city):
    api_key = "fc66389e2f74780ba0cc48f14a77ac16"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(complete_url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        
        if data["cod"] == 200:  # Check if the response is successful
            main = data["main"]
            weather_desc = data["weather"][0]["description"]
            temperature = main["temp"]
            speak(f"The temperature in {city} is {temperature} degrees Celsius with {weather_desc}.")
        else:
            speak("City not found. Please try again.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        speak("There was an error fetching the weather data. Please try again later.")

def get_current_datetime():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    current_date = now.strftime("%Y-%m-%d")
    speak(f"The current date is {current_date} and the time is {current_time}.")

def get_wikipedia_summary(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        speak(summary)
    except wikipedia.exceptions.DisambiguationError as e:
        speak("There are multiple results for that query. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("I couldn't find any information on that topic.")
    except Exception as e:
        speak("An error occurred while fetching the information.")

def main():
    speak("Hello! I am your voice assistant. How can I help you today?")
    
    while True:
        command = listen()
        
        if "weather" in command:
            speak("Which city do you want the weather for?")
            city = listen()
            get_weather(city)
        
        elif "date" in command or "time" in command:
            get_current_datetime()
        
        elif "wikipedia" in command:
            speak("What topic do you want to know about?")
            topic = listen()
            get_wikipedia_summary(topic)
        
        elif "exit" in command or "quit" in command:
            speak("Goodbye!")
            break
        
        else:
            speak("I can help you with the weather, current date and time, or information from Wikipedia. Just ask me!")

if __name__ == "__main__":
    main()
