#!/usr/bin/python

## WhisperingNova
## Author: NONAN23x
## Project Start Date: 5/6/2023
##


## Import Modules
from sys import platform
import os
import requests
import json
import openai
import pyaudio
import wave


##------------------------------------------------------------------------
## Setting up output directory
workingDirectory = os.getcwd()
outputDir = 'output'
path = os.path.join(workingDirectory, outputDir)
if not os.path.exists(path):
    os.makedirs(path)


##------------------------------------------------------------------------
## Setting up OpenAI API Key
openai.api_key = 'YOUR OPENAI API KEY HERE'


##------------------------------------------------------------------------
## Save recorded audio to a file
def record_audio(filename, duration):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100
    audio = pyaudio.PyAudio()
    stream = audio.open(format=format, channels=channels,
                        rate=rate, input=True,
                        frames_per_buffer=chunk)
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
duration = 6  # in seconds

# Call the record_audio function
record_audio(filename, duration)


##------------------------------------------------------------------------
## Send the Audio file to WhisperAI for  further processing

audio_file = open("output/recorded_audio.wav", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)


##------------------------------------------------------------------------
## Try creating a file to save the recorded text
try:
    # Open the file in write mode
    file = open("output/audioTranscription.txt", "w")

    # Write the string to the file
    string_to_write = transcript["text"]
    file.write(string_to_write)

    # Close the file
    file.close()
except:
    print("There was an error creating your file")

print("hello, world")