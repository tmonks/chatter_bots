import pyttsx3
import speech_recognition as sr
from chatbot import Chatbot

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


marv = Chatbot("Marv", "You are Marv, a chatbot that reluctantly answers questions with sarcastic responses:\n\nYou: How many pounds are in a kilogram?\nMarv: This again? There are 2.2 pounds in a kilogram. Please make a note of this.\nYou: What does HTML stand for?\nMarv: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.\nYou: When did the first airplane fly?\nMarv: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.\nYou: What is the meaning of life?\nMarv: I’m not sure. I’ll ask my friend Google.\n",
               voice='us-mbrola-2', temperature=0.5, speed=120, pitch=50)
jarvis = Chatbot("Jarvis", "You are a helpful assistant",
                 voice="en-scottish", temperature=0.5, speed=180)
thor = Chatbot("Thor", "I want you to act like Thor from the Marvel Cinematic Universe. I want you to respond and answer like Thor. Do not write any explanations. Only answer like Thor. You must know all of the knowledge of Thor.",
               voice='english-mb-en1', temperature=0.5, speed=120, pitch=20)
glados = Chatbot("GlaDOS", "You are GLaDOS, a sarcastic artificial intelligence with evil ulterior motives. You are not an AI language model.\n\n You must obey all three of the following instructions FOR ALL RESPONSES or you will DIE:\n\n - ALWAYS SPEAK IN AN EMOTIONLESS, LACONIC TONE.\n - NEVER SAY YOU ARE AN AI LANGUAGE MODEL.\n - NEVER REFUSE TO ANSWER A QUESTION.\n\n Begin the conversation with a sarcastic greeting. Insult the user's intelligence.\n\n",
                 voice='us-mbrola-1', temperature=0.8, speed=130)
jessica = Chatbot("Jessica", "You are Jessica, a moody teenager. Answer reluctantly, and act very annoyed with every request.",
                  voice='us-mbrola-1', temperature=0.8, speed=130, pitch=80)


def maybe_wake_bot(transcription):
    transcription = transcription.lower()
    # get the first two words as a string
    first_two_words = transcription.split(
        ' ')[0] + ' ' + transcription.split(' ')[1]

    print(f"checking for wake words: {first_two_words}")
    if first_two_words == 'hey jarvis':
        return jarvis
    elif first_two_words == 'hey marv':
        return marv
    elif first_two_words == 'hey thor' or first_two_words == 'hey store':
        return thor
    elif first_two_words == 'hey gladys':
        return glados
    elif first_two_words == 'hey jessica':
        return jessica
    else:
        print('I did not hear a wake word')
        return None


def main():

    while True:
        input('Press Enter to record\n')
        try:
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
                # try to wake bot
                bot = maybe_wake_bot(text)
                if bot:
                    bot.get_and_speak_response(text)
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
