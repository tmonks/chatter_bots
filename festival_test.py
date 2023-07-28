from speaker import Speaker
import os

# Path where Festival stores its voices
voice_path = "/usr/share/festival/voices/english"

# Get the list of subdirectories in the voice path
voices = [name for name in os.listdir(
    voice_path) if os.path.isdir(os.path.join(voice_path, name))]

print(voices)

# Test phrase
phrase = "This is a test of the festival voice system."

# Loop through the voices
for i, voice in enumerate(voices):
    speaker = Speaker(voice)
    print(f"Testing voice {i}: {voice}")
    speaker.speak(phrase)
