
import requests
import re

api_url = "http://127.0.0.1:5002/api/tts"



def remove_non_english_chars(input_string):
    # Define a regex pattern to match non-English characters
    # Exclude punctuation from removal
    pattern = re.compile('[^a-zA-Z0-9\s.,;!?\'"-]')
    
    # Use the pattern to replace non-English characters with an empty string
    cleaned_string = pattern.sub('', input_string)
    
    return cleaned_string



def tts(text, language='en'):
    try:
        text = text.strip()
        text = text.replace("\n", " ")
        #text = text.encode('utf-8')
        text = remove_non_english_chars(text)
        print(text)
        headers = {
            "text": text,
            "language-id": language
        }

        response = requests.post(api_url, headers=headers)
        
        return response.content
    except Exception as e:
        print("Exception in coqui_tts.py: {}".format(e))


if __name__ == '__main__':
    text = "I'm unable to provide information on that topic. 😕"
    print(text)
    tts(text)