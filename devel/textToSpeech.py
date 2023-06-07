#!/bin/python

import time
import requests
import sounddevice as sd
import soundfile as sf
import urllib


##------------------------------------------------------------------------
## Calculating the time required to run this code

startTime = time.time()

##------------------------------------------------------------------------
## send the text to VoiceVox and recieve japanese output
##------------------------------------------------------------------------
## Make Sure Docker is up and RUNNING!!!

# instantiate a audio file
def speak(sentence):

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

sentence = open('output/audioTranslation.txt', 'r')
speak(sentence.read())


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
## Calculating the time required to run this code

endTime = time.time()

totalTime =  abs(endTime - startTime)

print(f"Program has taken {totalTime} seconds to run")
