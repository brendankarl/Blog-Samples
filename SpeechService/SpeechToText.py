import requests

url = "https://REGION.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=en-us&format=detailed"
key = "KEY"
file_path = "C:/Weather.wav"
file_data = open(file_path, "rb").read()
headers = {"Ocp-Apim-Subscription-Key" : key,'Content-Type': 'Content-Type:audio/wav'}

r = requests.post(url,headers = headers, data=file_data)
result = r.json()
print(result["DisplayText"]) 
