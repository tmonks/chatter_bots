from dotenv import load_dotenv
from typing import Dict, List
from speaker import Speaker
from espeakng import ESpeakNG
import openai
import os
import re


# Set your OpenAI API key
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

MODEL_NAME = 'gpt-3.5-turbo'


class Chatbot:
    def __init__(self, name, system_prompt, voice='kal_diphone', temperature=0.5):
        self.name = name
        self.speaker = Speaker(voice)
        self.temperature = temperature
        self.messages = [{'role': 'system', 'content': system_prompt}]

    def get_and_speak_response(self, request_text):
        """Get response from OpenAI and speak it"""
        try:
            response = self._get_openai_response(request_text)
            response_content = self._speak_stream_response(response)
            self._append_message('user', request_text)
            self._append_message('assistant', response_content)
            return response_content
        except Exception as e:
            print(e)
            response_content = "I'm sorry, there was an error generating a response."
            self.speak(response_content)
            return response_content

    def _speak_stream_response(self, response):
        """Speak the streamed response from OpenAI in 'sentences'"""
        all_words = []
        words_in_sentence = []
        for chunk in response:
            self._append_word(chunk, words_in_sentence)
            self._append_word(chunk, all_words)

            if self._is_end_of_stream(chunk) or self._is_end_of_sentence(chunk):
                sentence = ''.join(words_in_sentence)
                print(sentence)
                self.speak(sentence)
                words_in_sentence = []

        return ''.join(all_words)

    def _get_openai_response(self, request_text):
        """Send request to OpenAI and return the streamed response"""
        user_message = {'role': 'user', 'content': request_text}

        return openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=self.messages + [user_message],
            temperature=self.temperature,
            stream=True
        )

    def speak(self, text):
        # remove any single or double quotes from the text
        text = re.sub(r'["\']', '', text)
        self.speaker.speak(text)

    def _create_message(self, role: str, content: str) -> Dict[str, str]:
        """Creates a message dictionary with a role and content"""
        return {'role': role, 'content': content}

    def _append_message(self, role: str, content: str) -> None:
        """Appends a message to the list of messages"""
        self.messages.append(self._create_message(role, content))

    def _is_end_of_sentence(self, chunk):
        """Takes a ChatCompletion stream chunk and returns True if the content ends a sentence"""
        word = chunk['choices'][0]['delta'].get('content', None)
        terminators = ['.', '!', '?', '\n', ',']

        # get the last character of the word
        if word and word[-1:] in terminators:
            return True
        else:
            return False

    def _is_end_of_stream(self, chunk):
        """Returns True if the stream chunk ends the has a finish_reason"""
        if chunk['choices'][0]['finish_reason']:
            return True
        return False

    def _append_word(self, chunk, words):
        """Appends a word to the list of words if it exists in the chunk"""
        word = chunk['choices'][0]['delta'].get('content', None)
        if word:
            words.append(word)
