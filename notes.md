# Notes

## Working of this program
1) To obtain Japanese Voice
    We can use VoiceVox application to generate realistic voices
    It can only use japanese text
    voicevox is a TEXT-TO-SPEECH-ENGINE

2) To obtain japanese text we use a translater, specifically we use
    GPT3.5, 
    GPT3.5 uses a english text, and outputs japanese text

3) To generate english text, we use whisper AI
    Whisper AI takes english speech and converts it to text
    Whisper AI is a SPEECH-TO-TEXT-ENGINE

## A quick algorithm
Voicevox(japanese text) - generate japansees voice
middleman that can feed japanese text to vioce vox is a
GPT(english text) - generates japanese text
final piece
whisperAI(souund file)

VoiceVox(GPT(WhisperAI(audio_file)))

## Running VoiceVox Engine
#### CPU
```
docker pull voicevox/voicevox_engine:cpu-ubuntu20.04-latest
docker run --rm -it -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-ubuntu20.04-latest
```
#### GPU
```
docker pull voicevox/voicevox_engine:nvidia-ubuntu20.04-latest
docker run --rm --gpus all -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:nvidia-ubuntu20.04-latest
```
#### Docker Pull Command
```
docker pull voicevox/voicevox_engine
```

## Running WhisperAI in docker for better latency
```
docker run -d -p 9000:9000 -e ASR_MODEL=base onerahmet/openai-whisper-asr-webservice:latest
```