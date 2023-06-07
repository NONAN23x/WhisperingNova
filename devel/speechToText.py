#!/bin/python

## Testing out different parts of code seperate to figure out sutff and cut down 
## transaction times

import pyaudio
import openai
import wave
import sys
import os
import time


##------------------------------------------------------------------------
## Calculating the time required to run this code

startTime = time.time()


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
## record audio from the mic

def record_audio(filename, duration):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100
    audio = pyaudio.PyAudio()
    stream = audio.open(format=format, channels=channels,
                        rate=rate, input=True,
                        frames_per_buffer=chunk)
    
    # Removing random text before output
    if (sys.platform == 'linux'):
        os.system('clear')
    else:
        os.system('cls')

    print("Recording started...")
    frames = []
    for i in range(int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    print("Recording completed.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio to a file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

# Specify the filename and duration of the recording
filename = 'output/recorded_audio.wav'
duration = 4  # in seconds

# Call the record_audio function
record_audio(filename, duration)


##------------------------------------------------------------------------
## Send the Audio file to WhisperAI for  further processing

def processAudio(audio_file):
    # set the global variable
    global transcript
    try:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    except:
        print("You need a working API Key")
        print("Exiting...")
        sys.exit(0)

audio_file = open("output/recorded_audio.wav", "rb")

# Send audio file to WhisperAI for audio processing
processAudio(audio_file)


##------------------------------------------------------------------------
## Try creating a file to save the recorded text

def createTextFile(file, transcript):
    try:
        # Write the string to the file
        string_to_write = transcript["text"]
        file.write(string_to_write)

        # Close the file
        file.close()
    except:
        print("There was an error creating your file")
        print("Exiting...")
        sys.exit(0)

# Open the file in write mode
file = open("output/audioTranscription.txt", "w")

# store the recieved transcript in a text file
createTextFile(file, transcript)

print(transcript['text'])

##------------------------------------------------------------------------
## Calulating the time taken to reach here

endTime = time.time()

timeTaken = endTime - startTime

print(f"Program took {timeTaken}s")