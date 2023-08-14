import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import io
import sounddevice

# Initialize recognizer
recognizer = sr.Recognizer()

# Set the energy threshold
recognizer.energy_threshold = 200


def transcribe_audio(audio):
    print('Attempting to transcribe audio...')
    try:
        transcription = recognizer.recognize_google(audio)
        return transcription
    except Exception as e:
        print(f'No speech recognized {e}')
        return None


def play_audio(audio):
    # convert speech_recognition AudioData to pydub AudioSegment
    audio_segment = AudioSegment.from_wav(io.BytesIO(audio.get_wav_data()))

    # play back audio
    print("Playing back audio...")
    play(audio_segment)


# Record audio from the microphone
with sr.Microphone() as source:
    # set pause threshold to 1 second
    source.pause_threshold = 1
    print("Please speak...")
    audio = recognizer.listen(source)

# Play back the recorded audio
play_audio(audio)

# Transcribe the audio to text
transcription = transcribe_audio(audio)
print(f"Transcription: {transcription}")
