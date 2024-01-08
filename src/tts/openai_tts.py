from openai import OpenAI
import os


api_key = os.getenv('OPENAI_KEY')

client = OpenAI(api_key=api_key)

response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Hello world! This is a streaming test.",
)

response.stream_to_file("output.mp3")