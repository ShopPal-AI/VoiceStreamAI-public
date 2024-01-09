
import requests

api_url = "http://127.0.0.1:5002/api/tts"



def tts(text, language='en'):
    try:
        text = text.strip()
        text = text.replace("\n", " ")
        headers = {
            "text": text,
            "language-id": language
        }

        response = requests.post(api_url, headers=headers)
        
        return response.content
    except Exception as e:
        print("Exception in coqui_tts.py: {}".format(e))


if __name__ == '__main__':
    tts("Understood! Here is my revised response:\n\nI appreciate your willingness to change. Can you please provide more details about what changes you would like to make and why?")