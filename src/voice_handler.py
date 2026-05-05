"""Voice Input/Output Handler Module"""

import speech_recognition as sr
import pyttsx3
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class VoiceHandler:
    """Handles voice input and output operations"""
    
    def __init__(self, enabled: bool = True):
        """Initialize voice handler"""
        self.enabled = enabled and os.getenv("VOICE_ENABLED", "true").lower() == "true"
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
        # Configure TTS
        rate = int(os.getenv("VOICE_RATE", "150"))
        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volume", 0.9)
        
    def listen(self, timeout: int = 10) -> Optional[str]:
        """Listen to microphone input and convert to text"""
        if not self.enabled:
            return None
            
        try:
            with sr.Microphone() as source:
                print("🎤 Listening... (speak now)")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=timeout)
                
            text = self.recognizer.recognize_google(audio)
            print(f"✓ Recognized: {text}")
            return text
            
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Error with speech recognition service: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error in voice input: {str(e)}")
            return None
    
    def speak(self, text: str):
        """Convert text to speech and play it"""
        if not self.enabled:
            return
            
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"Error in voice output: {str(e)}")
    
    def toggle_voice(self):
        """Toggle voice input/output"""
        self.enabled = not self.enabled
        status = "enabled" if self.enabled else "disabled"
        print(f"🔊 Voice {status}")
    
    def set_voice_language(self, language: str):
        """Set voice language"""
        try:
            self.recognizer.language = language
            logger.info(f"Voice language set to: {language}")
        except Exception as e:
            logger.error(f"Error setting language: {str(e)}")
