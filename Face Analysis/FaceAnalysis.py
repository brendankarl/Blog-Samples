from flask import Flask, render_template
from picamera import PiCamera
from time import sleep
import os
import random
import requests
import json

app = Flask(__name__)

@app.route('/')
def button():
    return render_template("button.html") # Presents a HTML page with a button to take a picture

@app.route('/takepic')
def takepic():
    currentdir = os.getcwd()
    randomnumber = random.randint(1,100) # A random number is created for a query string used when presenting the picture taken, this is to avoid web browser caching.
    camera = PiCamera()
    camera.start_preview()
    sleep(2)
    camera.capture(str(currentdir) + "/static/image.jpg") # Take a pic and store in the static directory used by Flask
    camera.close()
    url = "https://uksouth.api.cognitive.microsoft.com/face/v1.0/detect" # Replace with the Azure Congitive Services endpoint for the Face API (depends on the region deployed to)
    key = "" # Azure Cogntivie Services key
    image_path = str(currentdir) + "/static/image.jpg"
    image_data = open(image_path, "rb").read()
    headers = {"Ocp-Apim-Subscription-Key" : key,'Content-Type': 'application/octet-stream'}
    params = {
    'returnFaceId': 'false',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }
    r = requests.post(url,headers = headers,params = params, data=image_data) # Submit to Azure Cognitive Services Face API
    age = r.json()[0]["faceAttributes"]["age"] # Return the age of the first face
    gender = r.json()[0]["faceAttributes"]["gender"] # Return the gender of the first face
    haircolor = r.json()[0]["faceAttributes"]["hair"]["hairColor"][0]["color"] # Return the hair color of the first face
    emotions = r.json()[0]["faceAttributes"]["emotion"] # Return the emotions of the first face
    return render_template("FaceAnalysis.html",age=age,gender=gender,haircolor=haircolor,emotions=emotions,number=randomnumber) # Pass the results above to FaceAnalysis.html which presents the output and the pic taken to the user

if __name__ == "__main__":
    app.run(port=80,host='0.0.0.0')