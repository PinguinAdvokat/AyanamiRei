import requests
import json
import config


class Chat():
    def __init__(self, url, model, api_key, context_path):
        self.url = url
        self.model = model
        self.apiKey = api_key
        self.contextPath = context_path
        self.messages = get_context(context_path)
    
    def ask(self, text: str):
        self.messages.append({"role": "user", "content": text})
        resopnse = req(self.apiKey, self.model, self.url, self.messages)
        if resopnse.status_code == 200:
            self.messages.append(resopnse.json()["choices"][0]["message"])
            put_context(self.contextPath, self.messages)
            return resopnse.json()["choices"][0]["message"]["content"]
        else:
            print(resopnse)
        



def req(api, model, url, messages):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api}",
    }

    data = {
        "model": model,
        "messages": messages,
    }

    return requests.post(url, headers=headers, json=data, timeout=120)

def get_context(path: str):
    with open(path, "r", encoding="utf-8") as file:
        j = json.load(file, )
    return j

def put_context(path: str, context: list):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(context, f, ensure_ascii=False, indent=4)



chat = Chat(config.URL, config.MODEL, config.API_KEY, config.context_path)