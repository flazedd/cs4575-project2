import requests

headers = {
    "Content-Type": "application/json",
}

data = {
    'inputs':
'''You are interested in studying a rare type of breast cancer in a mouse model. 
Your research up until now has shown that the cancer cells show low expression of a key tumor suppressor gene. 
Which of these is the most suitable course of action to study the cause of gene silencing?''',

    'parameters': {
        'max_new_tokens': 2048,
        "temperature": 0.5,
    },
}

response = requests.post('http://127.0.0.1:8080/generate', headers=headers, json=data)
print(response.json())