#!/usr/bin/python

## Author: NONAN23x
## Project Start Date: 5/6/2023
# ██╗    ██╗██╗  ██╗██╗███████╗██████╗ ███████╗██████╗ ██╗███╗   ██╗ ██████╗ 
# ██║    ██║██║  ██║██║██╔════╝██╔══██╗██╔════╝██╔══██╗██║████╗  ██║██╔════╝ 
# ██║ █╗ ██║███████║██║███████╗██████╔╝█████╗  ██████╔╝██║██╔██╗ ██║██║  ███╗
# ██║███╗██║██╔══██║██║╚════██║██╔═══╝ ██╔══╝  ██╔══██╗██║██║╚██╗██║██║   ██║
# ╚███╔███╔╝██║  ██║██║███████║██║     ███████╗██║  ██║██║██║ ╚████║╚██████╔╝
#  ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ 
#                 
# ███╗   ██╗ ██████╗ ██╗   ██╗ █████╗ 
# ████╗  ██║██╔═══██╗██║   ██║██╔══██╗
# ██╔██╗ ██║██║   ██║██║   ██║███████║
# ██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║
# ██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║
# ╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝         
## VERSION: 1.0.23 beta


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
## Function to save recorded audio to a file
                                                                               
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
## Send the Audio file to WhisperAI docker instance for further processing

def make_asr_request(audio_file, docker_addr, asr_port_addr, language='en'):

    filename = audio_file
    base_url = f'http://{docker_addr}:{asr_port_addr}'
    print(base_url)

    with open(filename, 'rb') as f:
        file = {'audio_file': f}
        r = requests.post(f'{base_url}/asr?task=transcribe&language={language}&encode=true&output=json', files=file)
    return r.json()['text']


##------------------------------------------------------------------------
## Send the transcript to DeepL to recieve the translated text

def make_deepl_translate(text, docker_addr, deepl_port_addr, source_lang="EN", target_lang="JA"):

    base_url = f'http://{docker_addr}:{deepl_port_addr}'
    print(base_url)

    data = {"text": text,
                "source_lang": source_lang,
                "target_lang": target_lang}
    jsonData = json.dumps(data)
    r = requests.post(f'{base_url}/translate', data=jsonData)
    return r.json()['data']


##------------------------------------------------------------------------
## send the text to VoiceVox and receive japanese output

# instantiate a audio file
def store_response(sentence, docker_addr, voicevox_port, speaker_id):

    #specify base url
    base_url = f"http://{docker_addr}:{voicevox_port}"

    # generate initial query
    speakerID = speaker_id
    params_encoded  = urllib.parse.urlencode({'text': sentence, 'speaker': speakerID})
    r = requests.post(f'{base_url}/audio_query?{params_encoded}')
    voiceVox = r.json()
    voiceVox['volumeScale'] = 3.0
    voiceVox['intonationScale'] = 2.5
    voiceVox['prePhonemeLength'] = 0.1
    voiceVox['postPhonemeLength'] = 0.2
    voiceVox['speedScale'] = 0.85

    # making the api request
    params_encoded = urllib.parse.urlencode({'speaker': speakerID})
    r = requests.post(f'{base_url}/synthesis?{params_encoded}', json=voiceVox)
    with open("output/japaneseAudio.wav", 'wb') as outfile:
        outfile.write(r.content)


##------------------------------------------------------------------------
## Finally, play the obtained sound

def play_wav(filename):
    data, samplerate = sf.read(filename)
    sd.play(data, samplerate)
    sd.wait()


##------------------------------------------------------------------------
## Configuration fetching

def get_settings():
    try:
        with open('settings.json', 'r') as settings_file:
            settings = json.load(settings_file)
        return settings
    except FileNotFoundError:
        print("Settings file not found. Using default settings.")
        return {
            "docker_server_address": "127.0.0.1",
            "source_language_preference": "EN",
            "destination_language_preference": "JA",
        }


##------------------------------------------------------------------------
## Main code

def main():

    settings = get_settings()
    server_addr = settings["docker_server_address"]
    whisper = settings["whisper_ai_port"]
    voicevox = settings["voicevox_port"]
    deepl = settings['deepl_translator_port']


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
        transcript = make_asr_request(filename, server_addr, whisper)
    except:
        print("Error while making request to Whisper AI,")
        print("Do you have Docker running?")
        input("Press Enter to exit\n")
        sys.exit(0)

    print(transcript)


    try:
        global japaneseText
        japaneseText = make_deepl_translate(transcript, server_addr, deepl)
    except:
        print("Error when trying to reach DeepL")
        print("Do you have Docker running?")
        input("Press Enter to exit\n")
        sys.exit(0)
    print(japaneseText)

    try:
        store_response(japaneseText, server_addr, voicevox, speaker_id=10)
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
        print("Run the script in its folder!!!")
        input("Press Enter to exit\n")
        sys.exit(0)    


if __name__ == "__main__":
    main()
    