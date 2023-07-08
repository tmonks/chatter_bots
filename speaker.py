import subprocess


class Speaker:
    def __init__(self, voice="kal_diphone"):
        self.voice = voice

    def speak(self, text):
        # Write the command into a Scheme file
        with open('speech.scm', 'w') as f:
            f.write(f'(voice_{self.voice})\n(SayText "{text}")')

        # Run Festival with the Scheme file
        subprocess.run(['festival', '-b', 'speech.scm'])
