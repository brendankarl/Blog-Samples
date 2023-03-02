import requests
import json
import time

text = """The Sega Mega Drive, also known as the Sega Genesis in North America, was a popular video game console that was first released in Japan in 1988. 
It was Sega's third home console and was designed to compete with Nintendo's popular NES and SNES consoles. 
The Mega Drive was released in North America in 1989 and quickly gained a strong following among gamers thanks to its impressive graphics, sound quality, and large library of games. 
Some of the most popular games for the console include Sonic the Hedgehog, Streets of Rage, and Phantasy Star. 
The Mega Drive remained in production until 1997 and sold over 40 million units worldwide, cementing its place as one of the most beloved video game consoles of all time.""" # Text to be summarized

sentences = len(text.split(".")) / 2 # calculate how many sentences there are to be summarized (from the "text" variable), divide this by 2. Therefore if there are 6 setencnes to be summarised, the total number of sentences included in the summarization will be 3.

url = "https://ENDPOINT.cognitiveservices.azure.com/language/analyze-text/jobs?api-version=2022-10-01-preview" # Replace ENDPOINT with the relevant endpoint
key = "KEY" # Key for Azure Cognitive Services
headers = {"Ocp-Apim-Subscription-Key" : key}
payload = {
  "displayName": "Summarizer",
  "analysisInput": {
    "documents": [
      {
        "id": "1",
        "language": "en",
        "text": text
      }
    ]
  },
  "tasks": [
    {
      "kind": "ExtractiveSummarization",
      "taskName": "Summarizer",
      "parameters": {
        "sentenceCount": sentences
      }
    }
  ]
}

r = requests.post(url,headers = headers,data = json.dumps(payload))
results = r.headers["operation-location"]
time.sleep(10)
r = requests.get(results,headers = headers)

for s in r.json()["tasks"]["items"][0]["results"]["documents"][0]["sentences"]:
    print(s["text"])
