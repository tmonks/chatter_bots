from espeakng import ESpeakNG


def test_voices(voice):
    esng = ESpeakNG()
    esng.voice = voice
    print(f'Testing voice: {voice}')
    esng.say('Hello, this is a test of the eSpeak NG voice system.', sync=True)


def main():
    esng = ESpeakNG()
    voices = esng.voices

    # for voice in voices:
    #     print(voice)

    # Filter out all the English voices
    english_voices = [
        voice for voice in voices if voice['language'].startswith('en')]

    # for voice in english_voices:
    #     test_voices(voice['language'])

    for voice in ['mbrola-en1', 'mbrola-us1', 'mbrola-us2', 'mbrola-us3']:
        test_voices(voice)

        # If the voice has variants, test them too
        # if voice.variants:
        #     for variant in voice.variants:
        #         test_voices(f'{voice.name}+{variant}')


if __name__ == '__main__':
    main()
