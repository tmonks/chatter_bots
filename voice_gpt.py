import openai
import pyttsx3
import speech_recognition as sr
import time
from dotenv import load_dotenv
import os
from chatbot import Chatbot

# Set your OpenAI API key
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize the text-to-speech engine
# make sure to install espeak: `sudo apt install espeak`
engine = pyttsx3.init()


def transcribe_audio_to_text(filename):
    """Transcribes an audio file to text and returns the text."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print('Skipping unknown error')


def generate_response(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5
    )

    return response['choices'][0]['text']


def speak_text(text):
    """Speaks the given text."""
    engine.say(text)
    engine.runAndWait()


marv = Chatbot("Marv", "Directive1", "en-westindies", "male", 120, 100)
jarvis = Chatbot("Marv", "Directive1", "en-scottish", "male", 120, 120)


def maybe_wake_bot(transcription):
    print('I heard: ' + transcription)
    transcription = transcription.lower()
    if transcription == 'hey jarvis':
        return jarvis
    elif transcription == 'hey marv':
        return marv
    else:
        return None


def main():

    while True:
        # Wait for user to say "Jarvis"
        print('Say "Hey Jarvis" to start recording')
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                bot = maybe_wake_bot(transcription)
                if bot:
                    # record audio
                    filename = 'input.wav'
                    print('Say your question...')
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(
                            source, phrase_time_limit=None, timeout=None)
                        # write audio to file
                        with open(filename, 'wb') as f:
                            f.write(audio.get_wav_data())

                    # transcribe audio to text
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print('I heard: ' + text)
                        # generate response
                        # response = generate_response(text)
                        # print('GPT-3 response: ' + response)
                        # # speak response
                        # speak_text(response)
                        bot.speak(text)
            except Exception as e:
                print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
