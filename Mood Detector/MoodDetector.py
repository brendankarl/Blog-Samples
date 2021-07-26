from time import sleep
from picamera import PiCamera
from lobe import ImageModel
from flask import Flask, redirect, url_for, request, render_template
import csv
import datetime

app = Flask(__name__)

@app.route('/')
def button():
    return render_template('button.html') # Display the capture mood button, when clicked redirect to /capturemood

@app.route('/capturemood') # Take a pic, analyses and writes output to HTML and CSV
def capturemood():
    camera = PiCamera()
    camera.start_preview()
    sleep(2)
    camera.capture('mood.jpg') # Take picture using Raspberry Pi camera
    camera.close()

    model = ImageModel.load("Mood TFLite") # Load the ML model created using Lobe
    result = model.predict_from_file("mood.jpg") # Predict the mood of the mood.jpg pic just taken 
    now = datetime.datetime.now()
    date = now.strftime("%x")
    time = now.strftime("%X")
    moodCSV = open("Mood.csv", "a")
    moodCSVWriter = csv.writer(moodCSV) 
    moodCSVWriter.writerow([date,time,str(result.prediction)]) # Write the date, time and mood prediction to the Mood.csv file
    moodCSV.close()

    #Vary the HTML output depending on whether the prediction is positive or negative.
    if str(result.prediction) == "Negative": 
        return """<div class="buttons"><p>"Mood is Negative"</p>
        <a href='/capturemood'><input type='button' value='Capture Mood'></a></div>"""
    elif str(result.prediction) == "Positive":
        return """<div class="buttons"><p>"Mood is Positive"</p>
        <a href='/capturemood'><input type='button' value='Capture Mood'></a></div>"""

if __name__ == "__main__":
    app.run(port=80,host='0.0.0.0')