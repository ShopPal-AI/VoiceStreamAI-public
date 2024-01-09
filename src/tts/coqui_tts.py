
import requests

api_url = "http://127.0.0.1:5002/api/tts"



def tts(text, language='en'):
    text = text.strip()
    headers = {
        "text": text,
        "language-id": language
    }

    response = requests.post(api_url, headers=headers)
    
    return response.content


if __name__ == '__main__':
    tts("hi how are you")