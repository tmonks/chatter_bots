from espeakng import ESpeakNG

engine = ESpeakNG()

engine.voice = 'us-mbrola-2'
engine.speed = 120

text = "Hello, this is your computer speaking. How do I sound?"

# part1 = text.split()[:4]
# part2 = text.split()[4:]

parts = ['Knock knock.', 'Who\'s there?',
         'Doctor.', 'Doctor Who.', 'Haha,', 'I get it.']

for part in parts:
    engine.say(part, sync=True)

# engine.say(' '.join(part1), sync=True)
# engine.say(' '.join(part2), sync=True)
