import os
import speech_recognition as sr
from google import genai
from dotenv import load_dotenv
import time
from gtts import gTTS
from playsound import playsound
import threading
from pydub import AudioSegment
from pydub.playback import play

WAKE_WORD = os.getenv("WAKE_WORD")
LLM_MODEL = "gemini-2.5-flash"
SYSTEM_INSTRUCTION = os.getenv("SYSTEM_INSTRUCTION", "Tu es une IA copilote. Réponds de manière courte et concise.")
AUDIO_FILE = "response.mp3" 

load_dotenv() 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 

if not GEMINI_API_KEY:
    print("Error : La clé API Gemini n'est pas définie dans les variables d'environnement.")
    exit()

try:
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    print(f"Erreur d'initialisation du client Gemini : {e}")
    exit()

r = sr.Recognizer()

def speak(text):
    print(f"\n🤖 {WAKE_WORD} dit : {text}")
    
    def _speak_thread(t):
        try:
            tts = gTTS(text=t, lang='fr') 
            tts.save(AUDIO_FILE)
            
            sound = AudioSegment.from_file(AUDIO_FILE, format="mp3")

            play(sound)
            
        except Exception as e:
            print(f"⚠️ Erreur TTS/Playback : {e}")
        finally:
            if os.path.exists(AUDIO_FILE):
                os.remove(AUDIO_FILE)
    t = threading.Thread(target=_speak_thread, args=(text,))
    t.start()
    t.join()

def listen_for_wake_word(source):
    try:
        r.adjust_for_ambient_noise(source, duration=0.5) 
        print(f"👂 Écoute courte pour '{WAKE_WORD}'...")
        audio = r.listen(source, timeout=3, phrase_time_limit=3) 
    except sr.WaitTimeoutError:
        return None
    
    try:
        text = r.recognize_google(audio, language="fr-FR").lower()
        if WAKE_WORD.lower() in text:
            print(f"🟢 Wake Word détecté : {text}")
            return True
    except (sr.UnknownValueError, sr.RequestError):
        pass
    return False

def listen_for_command(source):
    speak("Oui? Je t'écoute.") 

    r.adjust_for_ambient_noise(source, duration=0.5)
    print("👂 Écoute longue pour la commande...")
    try:
        audio = r.listen(source, timeout=5, phrase_time_limit=10)
    except sr.WaitTimeoutError:
        return None

    try:
        command = r.recognize_google(audio, language="fr-FR")
        print(f"👤 L'utilisateur dit : {command}")
        return command
    except sr.UnknownValueError:
        speak("J'ai pas entendu, tu peux répéter ?")
        return None
    except sr.RequestError:
        speak("Mon micro a buggé, attends deux secondes.")
        return None

def get_llm_response(prompt):
    print("Envoi de la requête au LLM...")
    try:
        response = gemini_client.models.generate_content(
            model=LLM_MODEL, 
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.7
            )
        )
        return response.text
    except Exception as e:
        return f"Erreur lors de l'appel au LLM : {e}"


def main_loop():
    speak(f"Coucou, je suis {WAKE_WORD}, ton assistante IA. Dis mon nom pour me réveiller !")

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1) 
        
        while True:
            if listen_for_wake_word(source):
                command = listen_for_command(source) 
                
                if command:
                    if "stop" in command.lower() or "quitte" in command.lower() or "dors" in command.lower():
                        speak("Je me remets en veille.")
                        break

                    response = get_llm_response(command)
                    speak(response)
            
            time.sleep(0.1)


if __name__ == "__main__":
    main_loop()