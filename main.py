from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI()

audio_file = open("./output_chunks/chunk_1.wav", "rb")
transcription = client.audio.transcriptions.create(
    model="whisper-1", file=audio_file, response_format="text"
)
print(transcription)
