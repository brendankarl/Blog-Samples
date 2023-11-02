import requests
import pyautogui
import json
import time
from io import BytesIO
import os

time.sleep(10) # Giving sufficient time to launch the script in the background before launching the game

os.chdir('D:\\Development\\Typing of the Dead') # Update to local directory that stores the screenshot
      
def take_screenshot():
    pyautogui.screenshot('Screenshot.png')

def analyze_image(image):
    print("Analyzing screenshot...")
    url = "https://NAME.cognitiveservices.azure.com/vision/v3.0/read/analyze" # Replace NAME with the name of your instance
    key = "KEY" # Replace KEY with your Azure AI services key

    image_path = image
    image_data = open(image_path, "rb").read()

    headers = {"Ocp-Apim-Subscription-Key" : key,'Content-Type': 'application/octet-stream'}
    r = requests.post(url,headers = headers, data=image_data)

    operation_url = r.headers["Operation-Location"]

    # The recognized text isn't immediately available, so poll to wait for completion.
    analysis = {}
    poll = True
    while (poll):
        response_final = requests.get(r.headers["Operation-Location"], headers=headers)
        analysis = response_final.json()
        
        #print(json.dumps(analysis, indent=4))

        time.sleep(1)
        if ("analyzeResult" in analysis):
            poll = False
        if ("status" in analysis and analysis['status'] == 'failed'):
            poll = False

    lines = []
    for line in analysis["analyzeResult"]["readResults"][0]["lines"]:
        lines.append(line["text"])
    
    return(lines)

i = 1
while i == 1:
    take_screenshot()
    words = analyze_image("Screenshot.png")
    for word in words:
        pyautogui.write(word, interval=0.05)
    i += 1
