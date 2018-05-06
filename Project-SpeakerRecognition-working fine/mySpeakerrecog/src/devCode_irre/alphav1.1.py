import speech_recognition as sr

# get audio from the microphone
r = sr.Recognizer()

user_name = input("Enter username")
print("Welcome "+user_name)

with sr.Microphone() as source:
    print("Train...")
    print("Setup key-phrase to use as your password:")
    print("Speak:")
    print("listening...")
    audio1 = r.listen(source)
    key_phrase = r.recognize_google(audio1)
    print("Initializing authentication...")
    print("Speak:")
    print("listening...")
    audio = r.listen(source)

    voice_input = r.recognize_google(audio)

try:
    if voice_input == key_phrase:
        print("You said " + r.recognize_google(audio))
        print("Access granted")
    else:
        print("Access denied")
except sr.UnknownValueError:
    print("Could not understand audio")
except sr.RequestError as e:
    print("Could not request results; {0}".format(e))
