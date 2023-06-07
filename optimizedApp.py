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
    format = 'int16'
    channels = 1
    rate = 44100

    os.system('')  # Clear the console

    print("Recording started...")
    frames = sd.rec(int(duration * rate), samplerate=rate, channels=channels, dtype=format)
    sd.wait()
    print("Recording completed.")

    # Save the recorded audio to a file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(2)  # 2 bytes for 'int16' format
    wf.setframerate(rate)
    wf.writeframes(frames.tobytes())
    wf.close()

# Specify the filename and duration of the recording
filename = 'output/recorded_audio.wav'
duration = 4  # in seconds

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

audio_file = open("output/recorded_audio.wav", "rb")

# Send audio file to WhisperAI for audio processing
transcript = processAudio(audio_file)


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


def extract_text(json_data):
    pattern = r'"text"\s*:\s*"([^"]*)"'
    match = re.search(pattern, json_data)

    if match:
        text = match.group(1)
    else:
        text = ""

    return text

japaneseText = translate_text(transcript, "English", "Japanese")

sentence = extract_text(japaneseText)


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

store_response(sentence)


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
