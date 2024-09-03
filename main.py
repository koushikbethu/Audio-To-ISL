import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from itertools import count
import tkinter as tk
import string
import speech_recognition as sr

def listen_and_transcribe(language='en-US', timeout=3, energy_threshold=300, pause_threshold=0.5):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Please Wait!🙂 Preparing for the Audio Listening...")
        r.adjust_for_ambient_noise(source, duration=2)  
        r.energy_threshold = energy_threshold
        r.pause_threshold = pause_threshold 
        print("You Can Speak Now 🙂...")
        
        try:
            # Listen to the audio
            audio = r.listen(source, timeout=timeout)

            # Recognize the speech using Google's Web Speech API
            text = r.recognize_google(audio, language=language)
            return text
        
        except sr.RequestError as e:
            # API was unreachable or unresponsive
            return f"Could not request results from model; {e}"
        
        except sr.UnknownValueError:
            # Speech was unintelligible
            return "model could not understand audio"
        
        except sr.WaitTimeoutError:
            # No speech detected in the time limit
            return "No speech detected within the time limit"

def text_to_sign_language(input_text):
    isl_gif = ['any questions', 'are you angry', 'are you busy', 'are you hungry', 'are you sick', 'be careful',
               'can we meet tomorrow', 'did you book tickets', 'did you finish homework', 'do you go to office', 'do you have money',
               'do you want something to drink', 'do you want tea or coffee', 'do you watch TV', 'dont worry', 'flower is beautiful',
               'good afternoon', 'good evening', 'good morning', 'good night', 'good question', 'had your lunch', 'happy journey',
               'hello what is your name', 'how many people are there in your family', 'i am a clerk', 'i am bore doing nothing', 
               'i am fine', 'i am sorry', 'i am thinking', 'i am tired', 'i dont understand anything', 'i go to a theatre', 'i love to shop',
               'i had to say something but i forgot', 'i have headache', 'i like pink colour', 'i live in nagpur', 'lets go for lunch', 'my mother is a homemaker',
               'my name is john', 'nice to meet you', 'no smoking please', 'open the door', 'please call me later',
               'please clean the room', 'please give me your pen', 'please use dustbin dont throw garbage', 'please wait for sometime', 'shall I help you',
               'shall we go together tommorow', 'sign language interpreter', 'sit down', 'stand up', 'take care', 'there was traffic jam', 'wait I am thinking',
               'what are you doing', 'what is the problem', 'what is todays date', 'what is your father do', 'what is your job',
               'what is your mobile number', 'what is your name', 'whats up', 'when is your interview', 'when we will go', 'where do you stay',
               'where is the bathroom', 'where is the police station', 'you are wrong','address','agra','ahemdabad', 'all', 'april', 'assam', 'august', 'australia', 
               'badoda', 'banana', 'banaras', 'banglore', 'bihar','bridge','cat', 'chandigarh', 'chennai', 'christmas', 'church', 'clinic', 'coconut', 
               'crocodile','dasara','deaf', 'december', 'deer', 'delhi', 'dollar', 'duck', 'febuary', 'friday', 'fruits', 'glass', 'grapes', 'gujrat', 
               'hello', 'hindu', 'hyderabad', 'india', 'january', 'jesus', 'job', 'july', 'karnataka', 'kerala', 'krishna', 'litre', 'mango', 'may', 
               'mile', 'monday', 'mumbai', 'museum', 'muslim', 'nagpur', 'october', 'orange', 'pakistan', 'pass', 'police station', 'post office', 
               'pune', 'punjab', 'rajasthan', 'ram', 'restaurant', 'saturday', 'september', 'shop', 'sleep', 'southafrica', 'story', 'sunday', 
               'tamil nadu', 'temperature', 'temple', 'thursday', 'toilet', 'tomato', 'town', 'tuesday', 'usa', 'village', 'voice', 'wednesday', 'weight']
    
    arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    
    # Preprocess input text
    input_text = input_text.lower()
    input_text = ''.join([c for c in input_text if c not in string.punctuation])

    # Check if input text matches any predefined ISL phrases
    if input_text in isl_gif:
        class ImageLabel(tk.Label):
            """A label that displays images, and plays them if they are gifs"""
            def load(self, im):
                if isinstance(im, str):
                    im = Image.open(im)
                self.loc = 0
                self.frames = []

                try:
                    for i in count(1):
                        self.frames.append(ImageTk.PhotoImage(im.copy()))
                        im.seek(i)
                except EOFError:
                    pass

                try:
                    self.delay = im.info['duration']
                except:
                    self.delay = 100

                if len(self.frames) == 1:
                    self.config(image=self.frames[0])
                else:
                    self.next_frame()

            def unload(self):
                self.config(image=None)
                self.frames = None

            def next_frame(self):
                if self.frames:
                    self.loc += 1
                    self.loc %= len(self.frames)
                    self.config(image=self.frames[self.loc])
                    self.after(self.delay, self.next_frame)
        
        # Display corresponding GIF
        root = tk.Tk()
        lbl = ImageLabel(root)
        lbl.pack()
        lbl.load(f'ISL_Gifs/{input_text}.gif')
        root.mainloop()
    else:
        # Display individual letters quickly like a video
        fig, ax = plt.subplots()
        for char in input_text:
            if char in arr:
                ImageAddress = f'letters/{char}.jpg'
                ImageItself = Image.open(ImageAddress)
                ImageNumpyFormat = np.asarray(ImageItself)
                ax.imshow(ImageNumpyFormat)
                plt.draw()
                plt.pause(0.05)  # Reduced pause duration for faster display
                ax.clear()
        plt.close()

# Use the speech recognition input
transcribed_text = listen_and_transcribe()
print("Transcription:", transcribed_text)

if transcribed_text and "could not" not in transcribed_text.lower() and "could not understand" not in transcribed_text.lower():
    text_to_sign_language(transcribed_text)
else:
    print("There was an issue with the transcription.")
