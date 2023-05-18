import pyttsx3
from dotenv import load_dotenv
import openai
import os

# Set your OpenAI API key
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


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

    def generate_response(self, request_text):
        user_message = {'role': 'user', 'content': request_text}
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=self.messages + [user_message],
                temperature=self.temperature
            )

            print(response)
            response_content = response['choices'][0].message['content']
            self.messages.append(user_message)
            self.messages.append(
                {'role': 'assistant', 'content': response_content})
            return response_content
        except Exception as e:
            print(f"An error occurred: {e}")
            return "I'm sorry, there was an error generating a response."

    def get_and_speak_response(self, request_text):
        response = self.generate_response(request_text)
        self.speak(f'{self.name} says: {response}')

    def speak(self, text):
        # Use pyttsx3 library to speak the provided text
        self.engine.say(text)
        self.engine.runAndWait()
