import speech_recognition as sr

listener = sr.Recognizer()
try:
    with sr.Microphone() as source:
        print('listenting...')
        voice = listener.listen(source, phrase_time_limit= 5)
        print('reached')
        command = listener.recognize_google(voice)
        print(command)
except Exception as e:
    print(e)