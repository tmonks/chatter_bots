import pyttsx3


class Chatbot:
    def __init__(self, name, system_prompt, temperature, voice, speed):
        self.name = name
        self.voice = voice
        self.speed = speed
        self.temperature = temperature
        self.messages = [{'role': 'system', 'content': system_prompt}]

        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', self.voice)
        self.engine.setProperty('rate', self.speed)
        self.engine.setProperty('volume', 1.0)

    def get_and_speak_response(self, request_text):
        response = f'{self.name} says: {request_text}'
        self.speak(response)

    def speak(self, text):
        # Use pyttsx3 library to speak the provided text
        self.engine.say(text)
        self.engine.runAndWait()
