from gtts import gTTS
import pygame

def play_audio(file_path):
    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the mp3 file
    pygame.mixer.music.load(file_path)

    # Play the mp3 file
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# Text to be converted to speech
text = "Hello, how are you?"

# List of English accents
accents = ['com.au', 'co.uk', 'co.za', 'com', 'ca', 'co.in']

for accent in accents:
    # Create a gTTS object
    tts = gTTS(text=text, lang='en', tld=accent)

    # Save the speech audio into a file
    tts.save(f"output_{accent}.mp3")

