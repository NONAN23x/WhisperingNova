#!/bin/python

import requests
from pydub import AudioSegment
from pydub.playback import play

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
    voicevox_query['volumeScale'] = 4.0
    voicevox_query['intonationScale'] = 1.5
    voicevox_query['prePhonemeLength'] = 1.0
    voicevox_query['postPhonemeLength'] = 1.0

    # syntesize voice as wav file
    params_encoded = urllib.parse.urlencode({'speaker': speaker_id})
    r = requests.post(f'{base_url}/synthesis?{params_encoded}', json=voicevox_query)

    with open("output/japaneseAudio.wav", 'wb') as outfile:
        outfile.write(r.content)

sentence = open()
speak(sentence)


##------------------------------------------------------------------------
## Playing the obtained sound finally

song = AudioSegment.from_wav("output/japaneseAudio.wav")
play(song)
