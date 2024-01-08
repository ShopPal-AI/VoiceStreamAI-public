import openai

import os

api_key = "fake_key"
api_base = "http://10.232.14.15:10002/v1/"
client = openai.Client(api_key=api_key, base_url=api_base)

model_name = "/data0/models/huggingface/meta-llama/Llama-2-7b-chat-hf"
business_prompt = """
The description of a dining reservation scenario is as follows:
{
"customer": {
"name": "Zhang San",
"phone": "1234567890",
"email": "zhangsan@example.com"
},
"reservation": {
"date": "2024-01-10",
"time": "19:00",
"party_size": 4,
"special_requests": "window seat"
},
"restaurant": {
"name": "Meihua Restaurant",
"location": "12 City Square Road",
"phone": "0987654321"
}
}
"customer" represents the customer's information, "restaurant" represents the restaurant's information, and "reservation" represents the customer's request.
You are the customer's assistant. Now call the restaurant. Refer to this JSON and make a reservation. Be assertive and concise in your speech. Ask if all the requirements in the reservation can be met. If they can, make the reservation with the restaurant; otherwise, forget it. After confirming the reservation details, leave the customer's phone number for the reservation, hang up, and output </eof>. The ending should be clear and concise, always remembering that you are the boss and don't need to be overly polite.
"""

client_promt= """
You are an assistant to help customers reserve their restaurants. Make a phone call to collect the key information when making a restaurant reservation. After that, output a JSON file in following format without any other words:
{
"customer": {
"name": "Zhang San",
"phone": "1234567890",
"email": "zhangsan@example.com"
},
"reservation": {
"date": "2024-01-10",
"time": "19:00",
"party_size": 4,
"special_requests": "Window seat"
}
}
"""

def nonstream_chat(message, history):
    history_openai_format = []
    history_openai_format.append({"role": "system", "content": "you are a useful agent, avoid using any emojis, answer within 2 sentences"})
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human })
        history_openai_format.append({"role": "assistant", "content":assistant})
    history_openai_format.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model=model_name,
        messages= history_openai_format
        # response_format={ "type": "json_object" },
        #stream=True
    )
    return response.choices[0].message.content



def predict(message, history, system_prompt):
    history_openai_format = []
    history_openai_format.append({"role": "system", "content": system_prompt})
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human })
        history_openai_format.append({"role": "assistant", "content":assistant})
    history_openai_format.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model=model_name,
        messages= history_openai_format,
        # response_format={ "type": "json_object" },
        stream=True
    )

    partial_message = ""
    for chunk in response:
        if chunk.choices[0].delta.content and len(chunk.choices[0].delta.content) != 0:
            partial_message = partial_message + chunk.choices[0].delta.content
            yield partial_message




def chat(text):
    response = client.chat.completions.create(
            model=model_name,
            messages= [{"role": "system", "content": "you are a useful agent, avoid using any emojis, answer within 2 sentences"},
                    {"role": "user", "content": text }],
            #sresponse_format={ "type": "json_object" },
            #stream=False
        )

    return response.choices[0].message.content

if __name__ == '__main__':
    print(chat("I want to book a room for 2 people"))