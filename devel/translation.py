#!/bin/python

## Testing out different parts of code seperate to figure out sutff and cut down 
## transaction times

import openai
import sys
import os
import time
import re


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

system_message = {"role": "system", "content": "You are a helpful assistant that translates text."}


def translate_text(text, source_language, target_language):
    prompt = f"Translate the following '{source_language}' text to '{target_language}': {text}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            system_message,
            {"role": "user", "content": prompt + "\n\n I only want the Japanese Text, sound like a anime girl."}
        ],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    translation = response.choices[0].message.content.strip()
    translation = re.sub(r'\(.*', '', translation)
    return translation

transcript = str(input("Enter the text: "))


##------------------------------------------------------------------------
## Calculating the time required to run this code

startTime = time.time()


japaneseText = translate_text(transcript, "English", "Japanese")

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