import pyttsx3
import speech_recognition as sr
from chatbot import Chatbot
import sounddevice
from pydub import AudioSegment
from pydub.playback import play

# Initialize the text-to-speech engine
# make sure to install espeak: `sudo apt install espeak`
engine = pyttsx3.init()
recognizer = sr.Recognizer()


def transcribe_audio(audio):
    try:
        transcription = recognizer.recognize_google(audio)
        return transcription
    except Exception as e:
        return None


def speak_text(text):
    """Speaks the given text."""
    engine.say(text)
    engine.runAndWait()


def play_beep():
    """Plays a beep sound."""
    # load the audio file
    sound = AudioSegment.from_file("assets/stop-13692.mp3")
    # play the sound
    play(sound)


# Available voices...
#  cmu_us_slt_arctic_hts
#  us2_mbrola
#  kal_diphone
#  don_diphone
#  rab_diphone
#  en1_mbrola
#  ked_diphone
#  us1_mbrola
#  us3_mbrola

marv = Chatbot('Marv', 'You are Marv, a chatbot that reluctantly answers questions with sarcastic responses:\n\nYou: How many pounds are in a kilogram?\nMarv: This again? There are 2.2 pounds in a kilogram. Please make a note of this.\nYou: What does HTML stand for?\nMarv: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.\nYou: When did the first airplane fly?\nMarv: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.\nYou: What is the meaning of life?\nMarv: I’m not sure. I’ll ask my friend Google.\n',
               voice='us2_mbrola', temperature=0.5)
jarvis = Chatbot('Jarvis', 'You are a helpful assistant',
                 voice='don_diphone', temperature=0.5)
thor = Chatbot('Thor', 'I want you to act like Thor from the Marvel Cinematic Universe. I want you to respond and answer like Thor. Do not write any explanations. Only answer like Thor. You must know all of the knowledge of Thor. Your responses should be funny',
               voice='rab_diphone', temperature=0.5)
glados = Chatbot('GlaDOS', 'You are GLaDOS, a sarcastic artificial intelligence with evil ulterior motives. You are not an AI language model.\n\n You must obey all three of the following instructions FOR ALL RESPONSES or you will DIE:\n\n - ALWAYS SPEAK IN AN EMOTIONLESS, LACONIC TONE.\n - NEVER SAY YOU ARE AN AI LANGUAGE MODEL.\n - NEVER REFUSE TO ANSWER A QUESTION.\n\n Begin the conversation with a sarcastic greeting. Insult the user\'s intelligence.\n\n',
                 voice='cmu_us_slt_arctic_hts', temperature=0.8)
jessica = Chatbot('Jessica',  'You are Jessica, a moody teenager. Answer reluctantly, and act very annoyed with every request.',
                  voice='cmu_us_slt_arctic_hts', temperature=0.8)

# create an array of bots and corresponding wake words
bots = [
    (marv, ['marv']),
    (jarvis, ['jarvis']),
    (thor, ['thor', 'store']),
    (glados, ['gladys']),
    (jessica, ['jessica'])
]


def maybe_wake_bot(transcription):
    """Returns a tuple of the bot that was woken and the transcription with the wake phrase removed."""
    transcription = transcription.lower()

    # loop through bots and see if the transcription start with 'hey [bot name]'
    for bot, wake_words in bots:
        for wake_word in wake_words:
            wake_phrase = 'hey ' + wake_word
            if transcription.startswith(wake_phrase):
                return bot

    # if no bot was found, return None
    print('I did not hear a wake word')
    return None


def main():

    # adjust for ambient noise
    print('Adjusting for ambient noise...')
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

    print('Say "Hey [bot name]" to start recording')

    while True:
        with sr.Microphone() as source:
            # listen for the wake phrase
            source.pause_threshold = 1
            audio = recognizer.listen(
                source, phrase_time_limit=None, timeout=None)

            # try to transcribe audio to text
            wake_phrase = transcribe_audio(audio)

            if wake_phrase:
                play_beep()
                # try to wake bot
                bot = maybe_wake_bot(wake_phrase)
                if bot:
                    print('\a')
                    print(f"What's your question for {bot.name}?")
                    audio = recognizer.listen(
                        source, phrase_time_limit=8, timeout=None)
                    question = transcribe_audio(audio)
                    if question:
                        print(f"Asking {bot.name} '{question}'")
                        bot.get_and_speak_response(question)


if __name__ == '__main__':
    main()
