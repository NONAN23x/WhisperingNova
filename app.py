#!/usr/bin/python

## WhisperingNova
## Author: NONAN23x
## Project Start Date: 5/6/2023
###


# Import Modules
import requests
import json
import openai
import pyaudio
import wave


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
filename = 'recorded_audio.wav'
duration = 5  # in seconds

# Call the record_audio function
record_audio(filename, duration)


