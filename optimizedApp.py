#!/usr/bin/python

## WhisperingNova
## Author: NONAN23x
## Project Start Date: 5/6/2023


##------------------------------------------------------------------------
## Import Modules

import time
import sys
import os
import requests
import openai
import sounddevice as sd
import soundfile as sf
import wave
import urllib
import re
import pyaudio


##------------------------------------------------------------------------
## Setting up output directory

workingDirectory = os.getcwd()
outputDir = 'output'
path = os.path.join(workingDirectory, outputDir)
if not os.path.exists(path):
    os.makedirs(path)


##------------------------------------------------------------------------
## Setting up OpenAI API Key

openai.api_key = os.environ['OPENAIKEY']


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
## Runtime calculation start

startTime = time.time()


##------------------------------------------------------------------------
## Send the Audio file to WhisperAI for  further processing

def processAudio(audio_file):

    try:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript
    except:
        print("You need a working API Key")
        print("Exiting...")
        sys.exit(0)

audio_file = open(filename, "rb")

# Send audio file to WhisperAI for audio processing
transcript = processAudio(audio_file)

print(transcript)


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

japaneseText = translate_text(transcript, "English", "Japanese")


##------------------------------------------------------------------------
## send the text to VoiceVox and receive japanese output
##------------------------------------------------------------------------
## Make Sure Docker is up and RUNNING!!!

# instantiate a audio file

def store_response(sentence):

    #specify base url
    base_url = "http://127.0.0.1:50021"
    # generate initial query
    speaker_id = '10'
    params_encoded  = urllib.parse.urlencode({'text': sentence, 'speaker': speaker_id})
    r = requests.post(f'{base_url}/audio_query?{params_encoded}')
    voicevox_query = r.json()
    voicevox_query['volumeScale'] = 4.5
    voicevox_query['intonationScale'] = 2.5
    voicevox_query['prePhonemeLength'] = 0.1
    voicevox_query['postPhonemeLength'] = 0.3
    voicevox_query['speedScale'] = 0.8

    # syntesize voice as wav file
    params_encoded = urllib.parse.urlencode({'speaker': speaker_id})
    r = requests.post(f'{base_url}/synthesis?{params_encoded}', json=voicevox_query)

    with open("output/japaneseAudio.wav", 'wb') as outfile:
        outfile.write(r.content)

store_response(japaneseText)


##------------------------------------------------------------------------
## Playing the obtained sound finally

def play_wav(filename):
    data, samplerate = sf.read(filename)
    sd.play(data, samplerate)
    sd.wait()

# Specify the filename of the WAV file to play
filename = 'output/japaneseAudio.wav'

# Play the WAV file
play_wav(filename)


##------------------------------------------------------------------------
## Runtime calculation

endTime = time.time()

timeTaken = endTime - startTime

print(f"Program took {timeTaken} seconds")
