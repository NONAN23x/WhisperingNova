#!/bin/python

## Testing out different parts of code seperate to figure out sutff and cut down 
## transaction times

import openai
import sys
import os
import time
import requests
import json


##------------------------------------------------------------------------
## setup a output directory in this sub directory

workingDirectory = os.getcwd()
outputDir = 'output'
path = os.path.join(workingDirectory, outputDir)
if not os.path.exists(path):
    os.makedirs(path)


##------------------------------------------------------------------------
## setting up OpenAI Authentication

openai.api_key = os.environ['OPENAIKEY']


##------------------------------------------------------------------------
## Send the transcript to OpenAI to recieve the translated text

def make_deep_translate(text):
    base_url = 'http://localhost:8080'
    data = {"text": text,
                "source_lang": "EN",
                "target_lang": "JA"}
    jsonData = json.dumps(data)
    print(jsonData)
    r = requests.post(f'{base_url}/translate', data=jsonData)

    
    return r.json()['data']

transcript = str(input("Enter the text: "))


##------------------------------------------------------------------------
## Calculating the time required to run this code

startTime = time.time()


japaneseText = make_deep_translate(transcript)

print(japaneseText)

def createTextFile(file, transcript):
    try:
        # Write the string to the file
        string_to_write = transcript
        file.write(string_to_write)

        # Close the file
        file.close()
    except:
        print("There was an error creating your file")
        print("Exiting...")
        sys.exit(0)

# Open the file in write mode
file = open("output/audioTranslation.txt", "w")

# store the recieved transcript in a text file
createTextFile(file, japaneseText)


##------------------------------------------------------------------------
## Calculating the time required to run this code

endTime = time.time()

timeTaken = endTime - startTime

print(f"Program took {timeTaken}s")