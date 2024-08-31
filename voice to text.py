import speech_recognition as sr

def listen_and_transcribe(language='en-US', timeout=10, energy_threshold=4000):
    
    r = sr.Recognizer()

    
    with sr.Microphone() as source:
        print("Adjusting for ambient noise, please wait...")
        r.adjust_for_ambient_noise(source, duration=2)  
        r.energy_threshold = energy_threshold
        
        print("Listening...")
        
        try:
            # Listen to the audio
            audio = r.listen(source, timeout=timeout)  # Increased timeout to allow for longer speech

            # Recognize the speech using Google's Web Speech API
            text = r.recognize_google(audio, language=language)
            return text
        
        except sr.RequestError as e:
            # API was unreachable or unresponsive
            return f"Could not request results from Google Speech Recognition service; {e}"
        
        except sr.UnknownValueError:
            # Speech was unintelligible
            return "Google Speech Recognition could not understand audio"
        
        except sr.WaitTimeoutError:
            # No speech detected in the time limit
            return "No speech detected within the time limit"

# Test the transcription
print("Transcription:", listen_and_transcribe())
