import pyttsx3
import speech_recognition as sr
from chatbot import Chatbot
import sounddevice
from pydub import AudioSegment
from pydub.playback import play
import re

# Initialize the text-to-speech engine
# make sure to install espeak: `sudo apt install espeak`
engine = pyttsx3.init()
recognizer = sr.Recognizer()


def transcribe_audio(audio):
    print('Transcribing...')

    try:
        transcription = recognizer.recognize_google(audio)
        return transcription
    except Exception as e:
        print(f'No speech recognized {e}')
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


marv = Chatbot('Marv', 'You are Marv, a chatbot that reluctantly answers questions with sarcastic responses:\n\nYou: How many pounds are in a kilogram?\nMarv: This again? There are 2.2 pounds in a kilogram. Please make a note of this.\nYou: What does HTML stand for?\nMarv: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.\nYou: When did the first airplane fly?\nMarv: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.\nYou: What is the meaning of life?\nMarv: I’m not sure. I’ll ask my friend Google.\n',
               voice='cmu_us_aew_cg', temperature=0.5)
jarvis = Chatbot('Jarvis', 'You are a helpful assistant',
                 voice='cmu_us_awb_cg', temperature=0.5)
thor = Chatbot('Thor', 'I want you to act like Thor from the Marvel Cinematic Universe. I want you to respond and answer like Thor. Do not write any explanations. Only answer like Thor. You must know all of the knowledge of Thor. Your responses should be funny',
               voice='cmu_us_ahw_cg', temperature=0.5)
glados = Chatbot('GlaDOS', 'You are GLaDOS, a sarcastic artificial intelligence with evil ulterior motives. You are not an AI language model.\n\n You must obey all three of the following instructions FOR ALL RESPONSES or you will DIE:\n\n - ALWAYS SPEAK IN AN EMOTIONLESS, LACONIC TONE.\n - NEVER SAY YOU ARE AN AI LANGUAGE MODEL.\n - NEVER REFUSE TO ANSWER A QUESTION.\n\n Begin the conversation with a sarcastic greeting. Insult the user\'s intelligence.\n\n',
                 voice='cmu_us_ljm_cg', temperature=0.8)
jessica = Chatbot('Jessica',  'You are Jessica, a moody teenager. Answer reluctantly, and act very annoyed with every request.',
                  voice='cmu_us_eey_cg', temperature=0.8)

alex_prompt = """
You are a trivia question generator. 
The questions should be of a difficulty appropriate for ages 10-14 year olds.
Each question should have four possible answer, a through d.
I will respond with my guess and you will tell me if I'm correct or the correct answer, and provide the next question.
Whenever I say 'New topic', you should generate a new question on the topic I provide.
Continue generating questions on that topic until I tell you a different one."""

alex = Chatbot('Alex', alex_prompt, 'cmu_us_jmk_cg', temperature=0.8)

# create an array of bots and corresponding wake words
bots = [
    (marv, ['marv']),
    (jarvis, ['jarvis']),
    (thor, ['thor', 'store']),
    (glados, ['gladys']),
    (jessica, ['jessica']),
    (alex, ['alex'])
]


def maybe_wake_bot(original_transcription):
    """Returns a tuple of the bot that was woken and the transcription with the wake phrase removed."""
    transcription = original_transcription.lower()
    # if first word is 'hey', remove it
    transcription = re.sub(r'^hey ', '', transcription)

    # loop through bots and see if the transcription start with 'hey [bot name]'
    for bot, wake_words in bots:
        for wake_word in wake_words:
            if transcription.startswith(wake_word):
                # remove the wake phrase from the transcription with regex
                transcription = re.sub(rf'^{wake_word}\s?', '', transcription)
                return transcription, bot

    # if no bot was found, return None
    print('I did not hear a wake word')
    return original_transcription, None


def main():

    # adjust for ambient noise
    print('Adjusting for ambient noise...')
    with sr.Microphone() as source:
        # recognizer.adjust_for_ambient_noise(source, duration=1)
        # print(f'Ambient noise energy threshold: {recognizer.energy_threshold}')
        recognizer.energy_threshold = 200

    while True:
        print('\nListening for wake word...')
        with sr.Microphone() as source:
            # listen for the wake phrase
            source.pause_threshold = 1
            audio = recognizer.listen(source)

            # try to transcribe audio to text
            question_text = transcribe_audio(audio)

            if question_text:
                print(f'I heard: {question_text}')
                # try to wake bot
                question_text, bot = maybe_wake_bot(question_text)
                if bot:
                    play_beep()

                    # if question_text is empty, listen for a question
                    if not question_text:
                        print('Listening for question...')
                        audio = recognizer.listen(source, phrase_time_limit=10)
                        question_text = transcribe_audio(audio)

                    print(f"Asking {bot.name} '{question_text}'")
                bot.get_and_speak_response(question_text)


if __name__ == '__main__':
    main()
