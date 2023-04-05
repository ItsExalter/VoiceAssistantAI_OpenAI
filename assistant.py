import sys
import speech_recognition as sr
import pyttsx3 as tts
 
from neuralintents import GenericAssistant

import api_secret
import openai

# Make response as a Global Functions
response = ""

# Set API for OpenAI
openai.api_key = api_secret.API_KEY

# Set for Speech Recognition
recognizer = sr.Recognizer()

# Set for Text to Speech
speaker = tts.init()
speaker.setProperty('rate', 150)

# Set for Voice Preferences for Text to Speech
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[1].id) #it depends on the list of TTS on your devices

# Text to Speech Functions
def text_to_speech(text):
    speaker.say(text)
    speaker.runAndWait()
    speaker.stop()

# Call a Function to Check the Weather
def weather():
    print("It Works")

# Call a Function to Search VIA OpenAI
def openai_search():

    # Search in OpenAI
    result = openai.Completion.create(
            model="text-davinci-002", prompt=response, max_tokens=100
        )
    # Purge the Answer Result from OpenAI
    final_result = result["choices"][0]["text"].replace("\n", "")
    final_result = final_result.split("Chatbot:", 1)[0]

    # Set to TTS
    if final_result is not None:
        text_to_speech(final_result)

    
# Exit Session
def exit_session():
    text_to_speech("Goodbye, see you later!")
    sys.exit(0)

# Mapping the Functions for this Assistant
mappings = {
    "weather": weather,
    "search": openai_search,
    "exit": exit_session,
}

# Set the Intents and Train the Model
assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()

while True:
    try:
        # Start Mic Session
        with sr.Microphone() as mic:
            # Start Listening
            print("Listening... (press ctrl+c to stop)")
            recognizer.adjust_for_ambient_noise(mic, duration=3)
            audio = recognizer.listen(mic)
            print("Listening is stopped")

            # Change from the Audio into Text
            response = recognizer.recognize_google(
                audio, language="en-US", show_all=False
                )
            
            # Make the result is Lowercase
            response = response.lower()

        # Check the response
        if response is not None:
            # Call to Assistant Result
            response_text = assistant.request(response)
            # Check for the Response text
            if response_text is not None:
                text_to_speech(response_text)
    
    # Start Exception
    except sr.UnknownValueError:
        recognizer = sr.Recognizer()
        continue
