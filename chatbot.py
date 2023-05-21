from dotenv import load_dotenv
import openai
import os

from espeakng import ESpeakNG

# Set your OpenAI API key
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


class Chatbot:
    def __init__(self, name, system_prompt, voice='en', temperature=0.5, speed=150, pitch=50):
        self.name = name
        self.voice = voice
        self.speed = speed
        self.pitch = pitch
        self.temperature = temperature
        self.messages = [{'role': 'system', 'content': system_prompt}]

        self.engine = ESpeakNG()
        self.engine.voice = self.voice
        self.engine.speed = self.speed
        self.engine.pitch = self.pitch

    def generate_response(self, request_text):
        user_message = {'role': 'user', 'content': request_text}
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=self.messages + [user_message],
                temperature=self.temperature
            )

            response_content = response['choices'][0].message['content']
            print(response_content)
            self.messages.append(user_message)
            self.messages.append(
                {'role': 'assistant', 'content': response_content})
            return response_content
        except Exception as e:
            print(f"An error occurred: {e}")
            return "I'm sorry, there was an error generating a response."

    def get_and_speak_response(self, request_text):
        response = self.generate_response(request_text)
        self.speak(response)

    def speak(self, text):
        self.engine.say(text, sync=True)
