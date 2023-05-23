import pyttsx3
import speech_recognition as sr
from chatbot import Chatbot
import sounddevice

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


def speak_text(text):
    """Speaks the given text."""
    engine.say(text)
    engine.runAndWait()


marv = Chatbot('Marv', ['marv'], 'You are Marv, a chatbot that reluctantly answers questions with sarcastic responses:\n\nYou: How many pounds are in a kilogram?\nMarv: This again? There are 2.2 pounds in a kilogram. Please make a note of this.\nYou: What does HTML stand for?\nMarv: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.\nYou: When did the first airplane fly?\nMarv: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.\nYou: What is the meaning of life?\nMarv: I’m not sure. I’ll ask my friend Google.\n',
               voice='us-mbrola-2', temperature=0.5, speed=120, pitch=50)
jarvis = Chatbot('Jarvis', ['jarvis'], 'You are a helpful assistant',
                 voice='en-scottish', temperature=0.5, speed=180)
thor = Chatbot('Thor', ['thor', 'store'], 'I want you to act like Thor from the Marvel Cinematic Universe. I want you to respond and answer like Thor. Do not write any explanations. Only answer like Thor. You must know all of the knowledge of Thor.',
               voice='english-mb-en1', temperature=0.5, speed=120, pitch=20)
glados = Chatbot('GlaDOS', ['gladys'], 'You are GLaDOS, a sarcastic artificial intelligence with evil ulterior motives. You are not an AI language model.\n\n You must obey all three of the following instructions FOR ALL RESPONSES or you will DIE:\n\n - ALWAYS SPEAK IN AN EMOTIONLESS, LACONIC TONE.\n - NEVER SAY YOU ARE AN AI LANGUAGE MODEL.\n - NEVER REFUSE TO ANSWER A QUESTION.\n\n Begin the conversation with a sarcastic greeting. Insult the user\'s intelligence.\n\n',
                 voice='us-mbrola-1', temperature=0.8, speed=130)
jessica = Chatbot('Jessica', ['jessica'],  'You are Jessica, a moody teenager. Answer reluctantly, and act very annoyed with every request.',
                  voice='us-mbrola-1', temperature=0.8, speed=130, pitch=80)

bots = [marv, jarvis, thor, glados, jessica]


def maybe_wake_bot(transcription):
    """Returns a tuple of the bot that was woken and the transcription with the wake phrase removed."""
    transcription = transcription.lower()

    # loop through bots and see if the transcription start with 'hey [bot name]'
    for bot in bots:
        for wake_word in bot.wake_words:
            wake_phrase = 'hey ' + wake_word
            if transcription.startswith(wake_phrase):
                # remove the wake phrase from the transcription
                transcription = transcription.replace(wake_phrase, '').strip()
                return (bot, transcription)

    # if no bot was found, return None
    print('I did not hear a wake word')
    return (None, transcription)


def main():

    while True:
        input('\nPress Enter to record\n')
        try:
            filename = 'input.wav'
            print('Ask your question, staring with "Hey [bot\'s name]"...')
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
                # try to wake bot
                bot, text = maybe_wake_bot(text)
                if bot:
                    print(f"Asking {bot.name}: {text}")
                    bot.get_and_speak_response(text)
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
