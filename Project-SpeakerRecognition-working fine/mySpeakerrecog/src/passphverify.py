import speech_recognition as sr

r = sr.Recognizer()

def spchrcg(path, msg):
    with sr.WavFile(path) as source:  # use the default microphone as the audio source
        r.adjust_for_ambient_noise(source)  # listen for 1 second to calibrate the energy threshold for ambient noise levels
        audio = r.listen(source)  # now when we listen, the energy threshold is already set to a good value, and we can reliably catch speech right away

    try:
        said_phrase = r.recognize_google(audio)
        print("You said " + said_phrase)
        cnfrm = input("Confirm? Hit 'y' to continue or 'n' to retry")
        if cnfrm =='y':
            if said_phrase.lower() == msg.lower():
                print("Pass-phrase verified")
                return 0
            else:
                print("Access Denied! Wrong Pass-phrase")
                return 1
        elif cnfrm == 'n':
            return 1

    except LookupError:  # speech is unintelligible
        print("Could not understand audio")
        return 1

