#!/usr/bin/python

## WhisperingNova
## Author: NONAN23x
## Project Start Date: 5/6/2023
##


## Import Modules
import time
import sys
import os
import requests
import openai
import pyaudio
import wave
import urllib
import re
from pydub import AudioSegment
from pydub.playback import play


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
## Runtime calculation start

startTime = time.time()


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


##------------------------------------------------------------------------
## Send the transcript to an AI to recieve the translated text

def translate_text(text, source_language, target_language):
    prompt = f"Translate the following '{source_language}' text to '{target_language}': {text}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that translates text."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    translation = response.choices[0].message.content.strip()
    return translation

japaneseText = translate_text(transcript, "English", "Japanese")

def extract_text(json_data):
    pattern = r'"text"\s*:\s*"([^"]*)"'
    match = re.search(pattern, json_data)

    if match:
        text = match.group(1)
    else:
        text = ""

    return text

sentence = extract_text(japaneseText)
print(sentence)


##------------------------------------------------------------------------
## send the text to VoiceVox and recieve japanese output
##------------------------------------------------------------------------
## Make Sure Docker is up and RUNNING!!!

# instantiate a audio file
def speak(sentence):

    #specify base url
    base_url = "http://127.0.0.1:50021"
    # generate initial query
    speaker_id = '14'
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

speak(sentence)


##------------------------------------------------------------------------
## Playing the obtained sound finally

japaneseAudio = AudioSegment.from_wav("output/japaneseAudio.wav")
play(japaneseAudio)


##------------------------------------------------------------------------
## Runtime calculation

endTime = time.time()

timeTaken = endTime - startTime

print(f"Program took {timeTaken} seconds")