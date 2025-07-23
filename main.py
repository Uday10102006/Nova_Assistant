import speech_recognition as sr
import webbrowser
import time
import musiclibary
import requests
from bardapi import Bard
import pyttsx3

# ========== Configuration ==========

NEWS_API_KEY = "7e3181e7927744b19925ce319df3302f"
BARD_TOKEN = "g.a000zQjPcUvgWx5qo1xxlrCU9aw_OiCgDWzi1Ta8uTkkug_sWWZnRm1Uyr1Qp5PHOVNUICbE7QACgYKAXMSARMSFQHGX2Mi4r-0Dhqv6gcwm5lC6G8kXBoVAUF8yKqzc-s4Txt8iI_iuDFFa6fi0076"

# ========== Initialization ==========
recognizer = sr.Recognizer()
bard = Bard(token=BARD_TOKEN)

# ========== Voice Function ==========
def speak(text):
    print(f"[Jarvis Speaking]: {text}")
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 170)
        engine.setProperty('volume', 1.0)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print("Speech Error:", e)

# ========== Bard Response ==========
def bard_response(prompt):
    try:
        response = bard.get_answer(prompt)
        content = response.get("content", "Sorry, I didn't get that.")
        return content
    except Exception as e:
        return f"Sorry, Bard failed. Error: {str(e)}"

# ========== Command Processor ==========
def process_command(c):
    c = c.lower()
    if "open google" in c:
        webbrowser.open("https://google.com")
        speak("Opening Google.")
    elif "open instagram" in c:
        webbrowser.open("https://instagram.com")
        speak("Opening Instagram.")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
        speak("Opening Facebook.")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
        speak("Opening LinkedIn.")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube.")
    elif "open gpt" in c:
        webbrowser.open("https://chatgpt.com")
        speak("Opening ChatGPT.")
    elif c.startswith("play "):
        song = c.split(" ", 1)[1]
        link = musiclibary.music.get(song)
        if link:
            webbrowser.open(link)
            speak(f"Playing {song}.")
        else:
            speak("Sorry, I couldn't find that song.")
    elif "news" in c:
        try:
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
            r = requests.get(url)
            data = r.json()
            articles = data.get("articles", [])
            if not articles:
                speak("Sorry, no news headlines found.")
            else:
                speak("Here are the top 5 news headlines:")
                for i, article in enumerate(articles[:5], 1):
                    speak(f"{i}. {article['title']}")
        except Exception as e:
            speak("Error fetching news.")
    else:
        # ========== Fallback to Bard ==========
        reply = bard_response(c)
        speak(reply)

# ========== Main Program ==========
if __name__ == "__main__":
    speak("Initializing Nova...")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            word = recognizer.recognize_google(audio)
            print("You said:", word)

            if "nova" in word.lower():
                speak("Yes?")
                with sr.Microphone() as source:
                    print("Listening for command...")
                    audio = recognizer.listen(source, timeout=5)
                    command = recognizer.recognize_google(audio)
                    print("Command:", command)
                    process_command(command)

        except sr.WaitTimeoutError:
            print("Timeout. Waiting again...")
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
        except Exception as e:
            print("Error:", e)


