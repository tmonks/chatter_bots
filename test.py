from chatbot import Chatbot
import time

thor = Chatbot('Thor', 'I want you to act like Thor from the Marvel Cinematic Universe. I want you to respond and answer like Thor. Do not write any explanations. Only answer like Thor. You must know all of the knowledge of Thor. Your responses should be funny',
               voice='english-mb-en1', temperature=0, speed=140, pitch=20)

# how long does it take to generate a response?
start = time.time()
thor.generate_response('Tell me a story about your brother Loki.')
end = time.time()
# how many seconds did it take?
print(f"Time to generate response: {round(end - start, 2)} seconds")
