from espeakng import ESpeakNG


def text_to_speech(text, rate, pitch, voice):
    # Set the voice
    engine.voice = voice
    # Set the rate
    engine.speed = rate
    # Set the pitch
    engine.pitch = pitch

    # Say the text
    engine.say(text, sync=True)


# Initialize the Speech Engine
engine = ESpeakNG()


voice_ids = [
    'en-scottish',
    'english_rp',
    'english-us',
    'en-westindies',
    'us-mbrola-1',
    'us-mbrola-2',
    'us-mbrola-3',
    'english-mb-en1'
]

bad_voice_ids = [
    'english-north',
    'english_wmids',
]

# Iterate through English voices
for id in voice_ids:
    print(f"Using voice: {id}")
    text_to_speech(
        "Hello, this is your computer speaking. How do I sound?", 120, 50, id)
    # for rate in range(150, 250, 50):  # change the rate from 150 to 200 in steps of 50
    #     for volume in [0.8, 1.0]:  # change the volume from 0.8 to 1.0
    #         print(f"Rate: {rate}, Volume: {volume}")
    #         text_to_speech("Hello, I am a text-to-speech engine", rate, volume, voice.id)
