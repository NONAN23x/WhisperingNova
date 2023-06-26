#!/usr/bin/python


## WhisperingNova
## Author: NONAN23x
## Project Start Date: 5/6/2023
## VERSION: 1.0


##------------------------------------------------------------------------
## Import Modules

import os
import requests
import sounddevice as sd
import soundfile as sf
import wave
import urllib
import json
import pyaudio
import sys


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


##------------------------------------------------------------------------
## Send the Audio file to WhisperAI for  further processing

def make_asr_request(audio_file):
    base_url = 'http://localhost:9000'
    with open(filename, 'rb') as f:
        file = {'audio_file': f}
        r = requests.post(f'{base_url}/asr?task=transcribe&language=en&encode=true&output=json', files=file)
    return r.json()['text']


##------------------------------------------------------------------------
## Send the transcript to DeepL to recieve the translated text

def make_deep_translate(text, source_lang="EN", target_lang="JA"):
    base_url = 'http://localhost:8080'
    data = {"text": text,
                "source_lang": source_lang,
                "target_lang": target_lang}
    jsonData = json.dumps(data)
    r = requests.post(f'{base_url}/translate', data=jsonData)
    return r.json()['data']


##------------------------------------------------------------------------
## send the text to VoiceVox and receive japanese output

# instantiate a audio file
def store_response(sentence):
    #specify base url
    base_url = "http://127.0.0.1:50021"
    # generate initial query
    speaker_id = '10'
    params_encoded  = urllib.parse.urlencode({'text': sentence, 'speaker': speaker_id})
    r = requests.post(f'{base_url}/audio_query?{params_encoded}')
    voiceVox = r.json()
    voiceVox['volumeScale'] = 4.0
    voiceVox['intonationScale'] = 2.5
    voiceVox['prePhonemeLength'] = 0.1
    voiceVox['postPhonemeLength'] = 0.2
    voiceVox['speedScale'] = 0.84

    # making the api request
    params_encoded = urllib.parse.urlencode({'speaker': speaker_id})
    r = requests.post(f'{base_url}/synthesis?{params_encoded}', json=voiceVox)
    with open("output/japaneseAudio.wav", 'wb') as outfile:
        outfile.write(r.content)


##------------------------------------------------------------------------
## Playing the obtained sound finally

def play_wav(filename):
    data, samplerate = sf.read(filename)
    sd.play(data, samplerate)
    sd.wait()


##------------------------------------------------------------------------
## Main code

def main():

    # Creating output directory
    workingDirectory = os.getcwd()
    outputDir = 'output'
    path = os.path.join(workingDirectory, outputDir)
    try:
        if not os.path.exists(path):
           os.makedirs(path)
    except OSError:
        print(f"Error in creating directory: {OSError}")
        sys.exit(0)

    # Specify the filename and duration of the recording
    filename = 'output/recorded_audio.wav'
    duration = 5  # in seconds
    # Call the record_audio function
    try:
        record_audio(filename, duration)
    except:
        print('There was an error while recording your mic')
        input("Press Enter to exit")
        sys.exit(0)
    
    # Send audio file to WhisperAI for audio processing
    try:
        global transcript
        transcript = make_asr_request(filename)
    except:
        print("Error while making request to Whisper AI,")
        print("Do you have Docker running?")
        input("Press Enter to exit\n")
        sys.exit(0)

    print(transcript)


    try:
        global japaneseText
        japaneseText = make_deep_translate(transcript)
    except:
        print("Error when trying to reach DeepL")
        print("Do you have Docker running?")
        input("Press Enter to exit\n")
        sys.exit(0)
    print(japaneseText)

    try:
        store_response(japaneseText)
    except:
        print("Cannot communicate with VoiceVox...")
        print("Do you have Docker running?")
        input("Press Enter To exit\n")
        sys.exit(0)

    filename = 'output/japaneseAudio.wav'

    # Play the WAV file
    try:
        play_wav(filename)
        input("Press Enter to exit")
    except sd.PortAudioError:
        print("Error in detecting Audio Output Device")
        input("Press Enter to exit\n")
        sys.exit(0)
    except PermissionError:
        print("Error while playing the file, try choosing Desktop as the destination folder during setup")
        input("Press Enter to exit\n")
        sys.exit(0)    


if __name__ == "__main__":
    main()

