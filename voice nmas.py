# Print all available voices
import pyttsx3
engine = pyttsx3.init()

voices = engine.getProperty('voices')
for voice in voices:
    print(voice)
    engine.setProperty('voice', voice.id)
    engine.say("hello! world")
    engine.runAndWait()
