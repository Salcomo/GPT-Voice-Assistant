import openai
import pyttsx3
import speech_recognition as sr
import sounddevice as sd
import config

# Set up OpenAI API key
openai.api_key = config.OPENAI_API_KEY

def speechToText():
    """
    Uses the Google Speech Recognition API to transcribe speech to text from the user's microphone.
    Returns the transcribed text as a string.
    """
    # Initialize speech recognizer
    r = sr.Recognizer()
    
    # Listen to microphone input
    with sr.Microphone() as source:
        audio = r.listen(source)
        text = ""

        # Use Google Speech Recognition to transcribe audio
        try:
            text = r.recognize_google(audio)
            print("You said: " + text)
        except Exception as e:
            print("Exception: " + str(e))

    return text

def promptChatGPT(text):
    """
    Uses OpenAI's API to generate a response to the given prompt text.
    Returns the response as a string.
    """
    # Prompt the AI to generate a response using OpenAI's API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        temperature=0.7,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6)
    return response.choices[0].text

def speak(text):
    """
    Uses the pyttsx3 library to convert the input text to speech and speak it aloud.
    """
    # Initialize text-to-speech engine
    engine = pyttsx3.init()
    
    # Set the voice of the engine
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
    
    # Speak the input text
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    
    #Wake word detection
    WAKE = "hey computer"

    while True:
        print("Listening...")
        text = speechToText().lower()

        if text.count(WAKE) > 0:
            print("Woke up!")
            
            # Get user input
            userInput = speechToText()

            # Generate response
            response = promptChatGPT(userInput)

            # Convert response to speech
            speak(response)


