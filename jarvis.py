import time
import speech_recognition as sr
import pyttsx3
import requests

class Jarvis:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)  # Adjust the speech rate (150 is a moderate speed)
        self.engine.setProperty("volume", 100)  # Adjust the volume (1.0 is full volume)
        self.api_key = 'your_openai_api_key_here'
        self.wiki_api_key = 'your_wikipedia_api_key_here'

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self, timeout=None):
        with sr.Microphone() as source:
            print("Say something...")
            try:
                audio_input = self.recognizer.listen(source, timeout=timeout)
                text = self.recognizer.recognize_google(audio_input)
                return text.lower()
            except sr.WaitTimeoutError:
                print("Timeout. No speech detected.")
                return ""
            except sr.UnknownValueError:
                print("Speech recognition could not understand audio.")
                return ""
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                return ""

    def listen_timeout(self, timeout):
        start_time = time.time()
        while time.time() - start_time < timeout:
            user_input = self.listen(timeout=1)
            if "jarvis" in user_input:
                return self.listen()  # Continue listening until the user completes their sentence
        return ""

    def run(self):
        print("Hello! I am Jarvis. How can I assist you?")
        while True:
            user_query = self.listen_timeout(timeout=5)

            if user_query:
                self.speak("Please wait...")
                time.sleep(5)  # Wait for 5 seconds before confirming the command and answering questions

                if "search" in user_query:
                    query = user_query.replace("search", "").strip()
                    self.search_wikipedia(query)

            # Add more functions based on user queries as needed

    def search_wikipedia(self, query):
        endpoint = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
            "utf8": 1,
            "srlimit": 1,
            "formatversion": 2,
        }
        headers = {"Api-User-Agent": "Jarvis/1.0"}
        response = requests.get(endpoint, params=params, headers=headers)
        data = response.json()

        if "error" in data:
            print(f"Error: {data['error']['info']}")
            return

        if not data["query"]["search"]:
            print("No results found.")
            return

        result = data["query"]["search"][0]
        title = result["title"]
        snippet = result["snippet"]
        print(f"Search Result - Title: {title}\nSnippet: {snippet}")

    # Add more functions as needed

# Initialize and run Jarvis
jarvis = Jarvis()
jarvis.run()
