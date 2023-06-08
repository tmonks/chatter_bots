from dotenv import load_dotenv
import openai
import os
import time

from espeakng import ESpeakNG

# Set your OpenAI API key
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


def is_end_of_sentence(chunk):
    """Takes a ChatCompletion stream chunk and returns True if the content ends a sentence"""
    word = chunk['choices'][0]['delta'].get('content', None)
    terminators = ['.', '!', '?', '\n', ',']

    # get the last character of the word
    if word and word[-1:] in terminators:
        return True
    else:
        return False


def is_end_of_stream(chunk):
    """Returns True if the stream chunk ends the has a finish_reason"""
    if chunk['choices'][0]['finish_reason']:
        return True
    return False


def append_word(chunk, words):
    """Appends a word to the list of words if it exists in the chunk"""
    word = chunk['choices'][0]['delta'].get('content', None)
    if word:
        words.append(word)


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

    def get_and_speak_response(self, request_text):
        user_message = {'role': 'user', 'content': request_text}
        start = time.time()
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=self.messages + [user_message],
                temperature=self.temperature,
                stream=True,
            )

            all_words = []
            words_in_sentence = []
            for chunk in response:
                append_word(chunk, words_in_sentence)
                append_word(chunk, all_words)

                if is_end_of_stream(chunk) or is_end_of_sentence(chunk):
                    sentence = ''.join(words_in_sentence)
                    checkpoint = time.time()
                    print(f"{round(checkpoint - start, 2)}s: {sentence}")
                    self.speak(sentence)
                    words_in_sentence = []

            response_content = ''.join(all_words)

            self.messages.append(user_message)
            self.messages.append(
                {'role': 'assistant', 'content': response_content})
            return response_content
        except Exception as e:
            response_content = "I'm sorry, there was an error generating a response."
            self.speak(response_content)
            return response_content

    def speak(self, text):
        self.engine.say(text, sync=True)
