# Notes

## pyaudio build failed issue on linux
sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg
sudo pip install pyaudio

## Working of this program
1) To obtain Japanese Voice
    We can use VoiceVox application to generate realistic voices
    It can only use japanese text
    voicevox is a TEXT-TO-SPEECH-ENGINE

2) To obtain japanese text we use a translater, specifically we use
    DeepL translate, 
    Deep L translate uses a english text, and outputs japanese text

3) To generate english text, we use whisper AI
    Whisper AI takes english speech and converts it to text
    Whisper AI is a SPEECH-TO-TEXT-ENGINE


Voicevox(japanese text) - generate japansees voice
middleman that can feed japanese text to vioce vox is a
deepl(english text) - generates japanese text
final piece
whisperAI(souund file)

VoiceVox(DeepL(WhisperAI(audio_file)))