import sys
import threading
import tkinter as tk

import speech_recognition as sr
import pyttsx3 as tts
 
from neuralintents import GenericAssistant

import api_secret
import openai

class Assistant:
    
    openai.api_key = api_secret.API_KEY

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.speaker = tts.init()
        self.speaker.setProperty = ("rate", 150)

        self.assistant = GenericAssistant("intents.json", intent_methods={"weather": self.weather, "search": self.openai_search})
        self.assistant.train_model()

        self.root = tk.Tk()
        self.label = tk.Label(text="🔊", font=("Arial", 120, "bold"))
        self.label.pack()

        threading.Thread(target=self.run_assistant).start()

        self.root.mainloop()

    def openai_search(self, prompt):
        """Takes in a prompt string and uses OpenAI's GPT-3 model to generate a response.
        Returns the generated response as a string."""
        response = openai.Completion.create(
            model="text-davinci-002", prompt=prompt, max_tokens=1000
        )
        response_text = response["choices"][0]["text"].replace("\n", "")
        return response_text


    def weather(self):
        print("Success")

    def run_assistant(self):
        while True:
            try:
                with sr.Microphone() as mic:
                    self.recognizer.adjust_for_ambient_noise(mic, duration=1)
                    audio = self.recognizer.listen(mic)

                    text = self.recognizer.recognize_google(audio, language="en-US", show_all=False)
                    text = text.lower()

                    # So if Bob Called, Assitant will be called
                    if "hi bob" in text:
                        self.label.config(fg="red")
                        audio = self.recognizer.listen(mic)
                        text = self.recognizer.recognize_google(audio)
                        text = text.lower()
                        # Destroy Assistant if keyword stop called
                        if text == "stop":
                            self.speaker.say("Bye Bye Honey")
                            self.speaker.runAndWait()
                            self.speaker.stop()
                            self.root.destroy()
                            sys.exit(0)
                        
                        else:
                            if text is not None:
                                response = self.assistant.request(text)
                                if response is not None:
                                    self.speaker.say(response)
                                    self.speaker.runAndWait()

                            self.label.config(fg="black")

            except:
                self.label.config(fg="black")
                continue

Assistant()