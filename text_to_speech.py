import pyttsx3
import time

# Initialize the TTS engine globally (only once)
engine = pyttsx3.init()

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

        # Dummy run to ensure the first words aren't clipped
        engine.say(" ")
        engine.runAndWait()
        time.sleep(0.2)

        # Speak the main text
        engine.say(text)
        engine.runAndWait()

    except Exception as e:
        print(f"⚠️ TTS Error: {e}")


if __name__ == "__main__":
    # Example test
    speak_text("This is a test for text-to-speech using Staplr’s TTS engine.")
