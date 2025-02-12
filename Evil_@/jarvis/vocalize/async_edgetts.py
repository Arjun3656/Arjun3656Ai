import os
import sys

sys.path.insert(0, os.getcwd())

import edge_tts
import tempfile
import random
from playsound import playsound
from config import Config


phrases = [
    "The rest of the result has been printed to the chat screen, kindly check it out sir.",
    "The rest of the text is now on the chat screen, sir, please check it.",
    "You can see the rest of the text on the chat screen, sir.",
    "The remaining part of the text is now on the chat screen, sir.",
    "Sir, you'll find more text on the chat screen for you to see.",
    "The rest of the answer is now on the chat screen, sir.",
    "Sir, please look at the chat screen, the rest of the answer is there.",
    "You'll find the complete answer on the chat screen, sir.",
    "The next part of the text is on the chat screen, sir.",
    "Sir, please check the chat screen for more information.",
    "There's more text on the chat screen for you, sir.",
    "Sir, take a look at the chat screen for additional text.",
    "You'll find more to read on the chat screen, sir.",
    "Sir, check the chat screen for the rest of the text.",
    "The chat screen has the rest of the text, sir.",
    "There's more to see on the chat screen, sir, please look.",
    "Sir, the chat screen holds the continuation of the text.",
    "You'll find the complete answer on the chat screen, kindly check it out sir.",
    "Please review the chat screen for the rest of the text, sir.",
    "Sir, look at the chat screen for the complete answer.",
]


def play_audio(audio_bytes: bytes) -> None:
    """
    Play audio directly from bytes.

    Args:
        audio_bytes (bytes): Audio data to be played.
    """
    # Write bytes to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file.write(audio_bytes)
        audio_file_path = tmp_file.name

    # Play the audio using playsound
    playsound(audio_file_path)


async def fetchAudio(
    text, assistantVoice=Config.ASSISTANT_VOICE, pitch="+0Hz", rate="+0%"
) -> bytes:
    """
    Fetch audio from TTS service

    Args:
        text (str): text to convert
        AssistantVoice (str, optional): Voice. Defaults to "ASSISTANT_VOICE".
        pitch (str, optional): pitch. Defaults to '0Hz'. [-100, +100]Hz
        rate (str, optional): rate. Defaults to '0%'. [-100, +100]%
    """
    try:
        communicate = edge_tts.Communicate(text, assistantVoice, pitch=pitch, rate=rate)
        audioBytes = b""
        async for element in communicate.stream():
            if element["type"] == "audio":
                audioBytes += element["data"]
        return audioBytes
    except Exception as e:
        print(e)
        return b""


async def textToSpeechBytes(text: str, assistantVoice=Config.ASSISTANT_VOICE) -> bytes:
    return await fetchAudio(text, assistantVoice)


async def text_to_speech(text: str) -> None:

    text_chunks = text.split(".")

    if len(text_chunks) > 4 and len(text) >= 250:
        text = " ".join(text_chunks[:2]) + ". " + random.choice(phrases)

    audioBytes = await textToSpeechBytes(text)
    play_audio(audioBytes)


if __name__ == "__main__":
    import asyncio

    text = "Hello, how are you?"
    audioBytes = asyncio.run(textToSpeechBytes(text))
    play_audio(audioBytes)
