# Script that analyses the transcript output from the OCI AI Speech service

import json

# Open the transcription JSON output file
filepath = "/users/bkgriffi/Downloads/transcript.json" # Location of the transcription output JSON file
transcriptsource = open(filepath)

# Read the transcription
transcriptJSON = json.load(transcriptsource)
transcriptJSON["transcriptions"][0]["transcription"] # This is looking at the output of the first transciption within the output, denoted by 0. If transcribing multiple videos within a single job, this would need to be updated accordingly.

for word in transcriptJSON["transcriptions"][0]["tokens"]:
    if word["confidence"] < '0.70':
        if word["token"] not in ('.',','):
            print(word["token"] + " - " + "Confidence: " + word["confidence"] + " at: " + word["startTime"])


for word in transcriptJSON["transcriptions"][0]["tokens"]:
    if word["confidence"] < '0.70': # Only display words with a detection confidence of less than 70%
        if word["token"] not in ('.',','): # Exclude full stops and commas
            print(word["token"] + " - " + "Confidence: " + word["confidence"] + " at: " + word["startTime"])

