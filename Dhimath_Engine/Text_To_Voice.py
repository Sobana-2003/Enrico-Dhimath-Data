import pyttsx3

def speak(text, gender):

    engine = pyttsx3.init()
    voices = engine.getProperty('voices') 
    if gender == "F":
        engine.setProperty('voice', voices[1].id) 
    else:
        engine.setProperty('voice', voices[0].id)
    volume = engine.getProperty('volume')
    engine.say(text)
    engine.runAndWait() 