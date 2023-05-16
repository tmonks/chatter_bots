import pyttsx3


class Chatbot:
    def __init__(self, name, directive, voice, gender, speed, pitch):
        self.name = name
        self.directive = directive
        self.voice = voice
        self.gender = gender
        self.speed = speed
        self.pitch = pitch

        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", self.speed)
        self.engine.setProperty("volume", 1.0)
        self.engine.setProperty("pitch", self.pitch)

    def respond(self, request_text):
        response = self.generate_response(request_text)
        self.speak(response)

    def generate_response(self, request_text):
        # Your logic to generate a response based on the request_text
        # This can be as simple or complex as you want, using conditionals or machine learning models.

        # For example, a simple echo response
        return f"{self.name} says: {request_text}"

    def speak(self, text):
        # Use pyttsx3 library to speak the provided text
        self.engine.setProperty("voice", self.voice)
        self.engine.say(text)
        self.engine.runAndWait()
