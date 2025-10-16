import pyttsx3
import time # Time is no longer strictly necessary, but kept for convention

# Initialize the TTS engine globally (only once)
# This is generally the correct approach for performance
try:
    engine = pyttsx3.init()
except Exception as e:
    print(f"FATAL ERROR: Could not initialize pyttsx3 engine. Check your installation and audio drivers.")
    print(f"Details: {e}")
    # You might want to exit here if initialization fails completely
    # exit() 


def speak_text(text: str, rate: int = 175, voice: str = None):
    """
    Speak the given text aloud using the pyttsx3 TTS engine.

    Args:
        text (str): The text to be spoken.
        rate (int, optional): Speech rate (default: 175).
        voice (str, optional): Voice ID (if available on the system).
    """
    if not text.strip():
        print("⚠️ No text provided to speak.")
        return

    try:
        # Configure TTS properties
        engine.setProperty("rate", rate)
        if voice:
            engine.setProperty("voice", voice)

        # Speak the main text
        # This queues the text for speech
        engine.say(text)
        
        # This command blocks until all queued speech commands are complete
        engine.runAndWait()

    except Exception as e:
        print(f"⚠️ TTS Error during speech: {e}")


if __name__ == "__main__":
    # --- Troubleshooting Tip: List Voices ---
    # This helps confirm the engine is working and you have voices available
    voices = engine.getProperty('voices')
    print(f"Total voices found: {len(voices)}")
    if voices:
        print(f"Using default voice: {voices[0].id}")
        # To use a specific voice, you can set it like this:
        # VOICE_ID = voices[0].id 

    # Example test
    print("Speaking now...")
    speak_text("This is a test for text-to-speech using the pyttsx3 engine. If you hear this, the fix worked.")
    
    # Optional: Test with a different rate
    speak_text("Testing a slightly slower speed.", rate=150)

    # Clean up the engine after all speech is done
    engine.stop()
    print("Speech completed and engine stopped.")
