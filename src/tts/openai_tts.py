from openai import OpenAI
import os


api_key = os.getenv('OPENAI_KEY')

#client = OpenAI(api_key=api_key)
client = OpenAI(api_key='inner-token-5tmzLnYfHKRk62zwrJShFhWbT6vf8Z4Q', base_url='https://gateway.ai.buildagi.dev/v1/dreampal/openai/v1/')


def tts(text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )

    data = bytearray()
    for chunk in response.iter_bytes():
        data.extend(chunk)
    return data

if __name__ == '__main__':
    tts("Hey there! \ud83d\ude0a How can I help you today?")