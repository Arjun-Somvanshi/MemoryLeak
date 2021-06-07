from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty
from functools import partial
from icecream import ic
import speech_recognition as sr
import telenium
from kivy.clock import Clock

Window.clearcolor = (0, 0, 0, 0.25)

listener = sr.Recognizer()
kv = '''
Screen_Manager:
    SpeechScreen:
    PracticeScreen:

<SpeechScreen>:
    name: 'speechscreen'
    BoxLayout:
        canvas.before:
            Color:
                rgba: (0.15, 0.15, 0.15, 1)
            Rectangle:
                pos: self.pos
                size: self.size
        orientation: 'vertical'
        padding: dp(25)
        spacing: dp(10)
        TextInput:
            id: speech
            text: 'Hello my fellow employees. Today is a great day for our company as we lauch the new model of BMW'            
            hint_text: 'Enter The Speech' 
            multiline: True
        TextInput:
            id: wpm
            text: '130'
            hint_text: 'Words Per Minute'
            size_hint_y: None
            height: dp(60)
        Button:
            id: save
            size_hint: 0.5, 0.2
            pos_hint: {'center_x': 0.5}
            text: 'Save'
            on_release:
                app.root.current = 'practicescreen'             
                app.speech = speech.text   
                root.calculate_time()
<PracticeScreen>:
    name: 'practicescreen'
    BoxLayout:
        canvas.before:
            Color:
                rgba: (0.15, 0.15, 0.15, 1)
            Rectangle:
                pos: self.pos
                size: self.size
        orientation: 'vertical'
        Label:
            text: root.speech_text
            font_size: sp(20)
        Label:
            id: result
            text: ''
            size_hint_y: 0.2
        Button:
            size_hint: 0.5, 0.15
            pos_hint: {'center_x': 0.5}
            text: 'Listen'
            on_release: root.listen()

'''

class Screen_Manager(ScreenManager):
    pass


class SpeechScreen(Screen):
    def parser(self):
        self.ids.speech.text.split('.')
    def calculate_time(self):
        print("This button was pressed through automation")
        global app
        app.time = self.time_calc(self.ids.speech.text)
        print("This is the time: ", app.time)
    
    def time_calc(self, text): 
        text_len =  len(text.replace('.','').split(' '))
        text_time = (text_len/int(self.ids.wpm.text))*60
        return text_time
            

class PracticeScreen(Screen):
    speech_text = StringProperty('')
    def listen(self):
        global app
        try:
            with sr.Microphone() as source:
                print('listenting...')
                voice = listener.listen(source, phrase_time_limit = app.time)
                print('reached')
                self.speech_text = listener.recognize_google(voice)
                print(self.speech_text)
                misspoken, speech_time_compare = self.compare(app.speech, self.speech_text)
                print(misspoken, speech_time_compare)

        except Exception as e:
            print(e)

    def compare(self, text, speech):
        text = text.strip().lower()
        speech = speech.strip().lower()
        text_words = text.replace('.','').split(' ')
        speech_words = speech.split(' ')
        misspoken = []
        for (tword, sword) in zip(text_words, speech_words):
            if tword != sword:
                misspoken.append([sword, tword])
        speech_time_compare = (len(text_words) == len(speech_words))
        print(len(speech_words), len(text_words))
        for miss in misspoken:
            self.ids.result.text = 'You said ' + miss[0] + ' instead of ' + miss[1] + '\n'
        if not speech_time_compare:
            self.ids.result.text += 'You could not finish in time!!!'
        return misspoken, speech_time_compare
    
   

class MemoryLeakApp(App):
    speech = StringProperty('')
    time = NumericProperty(0)
    def build(self):
        global app 
        app = self
        return Builder.load_string(kv)
    def on_start(self):
        Clock.schedule_once(self.testmodule, 3)
    def testmodule(self, dt):
        tc = "server.connect"
        print("This is the start of the automated function tests")
        print("The following are the test cases for the given text inputs")
        ic("testcase1: Speech = empty string, WPM = 100")
        ic("testcase2: Speech = 'Hello World', WPM = empty string")
        ic("testcase3: Speech = empty string, WPM = empty string")
        ic("testcase4: Speech = 'Hello World', WPM = '123@!ABDCGG'")
        Clock.schedule_once(partial(self.numeric_checks, '', 100, 1))
        Clock.schedule_once(partial(self.numeric_checks, 'Hello World', '', 2))
        Clock.schedule_once(partial(self.numeric_checks, '', '', 3))
        Clock.schedule_once(partial(self.numeric_checks, 'Hello World', '123@!ABDCGG', 4))
        Clock.schedule_once(partial(self.numeric_checks, 'Hello World', '140', 5))

    def numeric_checks(self, speech, wpm, testcase, dt):
        if speech != '':
            if wpm.isnumeric():
                result = f'testcase{testcase} has passed'
                ic(result)
            else:
                if wpm == '':
                    result = f'WPM attribute cannot allow empty strings, testcase{testcase} failed'
                    ic(result)
                else:
                    result = f'WPM attribute cannot allow non numeric strings, testcase{testcase} failed'
                    ic(result)
        else:
            result = f'speech attribute cannot allow empty strings, testcase{testcase} failed'
            ic(result)

        
MemoryLeakApp().run()
