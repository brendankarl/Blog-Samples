import requests
import json
import time
from io import BytesIO
from picamera import PiCamera
from gpiozero import MotionSensor

pir = MotionSensor(4)
          
def take_image():
    print("Taking photo of reg plate...")
    camera = PiCamera()
    camera.rotation = 180 # depending on how the camera is placed, this line may need to be removed
    camera.start_preview()
    time.sleep(3)
    camera.capture("regplate.jpg")
    camera.stop_preview()
    camera.close() 
    print("Photo taken successfully!")

def analyze_image(image):
    print("Analyzing photo...")
    url = "https://REPLACEME.cognitiveservices.azure.com/vision/v3.0/read/analyze" # Endpoint URL for Azure Cognitive Services
    key = "KEY" # Key for Azure Cognitive Services

    image_path = image
    image_data = open(image_path, "rb").read()

    headers = {"Ocp-Apim-Subscription-Key" : key,'Content-Type': 'application/octet-stream'}
    r = requests.post(url,headers = headers, data=image_data)

    operation_url = r.headers["Operation-Location"]
    
    analysis = {}
    poll = True
    while (poll):
        response_final = requests.get(r.headers["Operation-Location"], headers=headers)
        analysis = response_final.json()

        time.sleep(1)
        if ("analyzeResult" in analysis):
            poll = False
        if ("status" in analysis and analysis['status'] == 'failed'):
            poll = False

    lines = []
    for line in analysis["analyzeResult"]["readResults"][0]["lines"]:
        lines.append(line["text"])

    print("-Reg plate analyzed as " + str(lines[0].replace(" ",""))) # Report the first string detected in the analysis - this may need to be tweaked

while True:
    print("Waiting for car...")
    pir.wait_for_motion()
    print("Car detected!")
    time.sleep(2)
    take_image()
    reg = analyze_image("regplate.jpg")
    pir.wait_for_no_motion()
