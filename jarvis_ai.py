import speech_recognition as sr # type: ignore
import pyttsx3 # type: ignore
import openai # type: ignore
import datetime
import webbrowser
import os

# === CONFIGURE YOUR OPENAI API KEY HERE ===
openai.api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Replace with your key

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand.")
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
        return ""

def ask_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or use "gpt-4" if you have access
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message['content'].strip()
        return answer
    except Exception as e:
        return "There was an error reaching OpenAI."

def run_jarvis():
    speak("Hello Vikas. Jarvis is now online.")
    while True:
        command = listen()

        if not command:
            continue

        if "stop" in command or "exit" in command or "shutdown" in command:
            speak("Shutting down. Have a great day, Vikas!")
            break

        elif "time" in command:
            now = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {now}.")

        elif "open youtube" in command:
            speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")

        elif "open google" in command:
            speak("Opening Google.")
            webbrowser.open("https://www.google.com")

        elif "open vs code" in command:
            path = r"C:\Users\YourName\AppData\Local\Programs\Microsoft VS Code\Code.exe"  # Change path
            os.startfile(path)
            speak("Opening Visual Studio Code.")

        elif "who is" in command or "what is" in command or "define" in command or "explain" in command:
            speak("Let me think...")
            answer = ask_openai(command)
            speak(answer)

        else:
            speak("Let me try to answer that using OpenAI.")
            answer = ask_openai(command)
            speak(answer)

# === Run your AI Assistant ===
run_jarvis()
