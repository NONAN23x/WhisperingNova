![alt text](images/whisperingNova.png "WhisperingNova")

# WhisperingNova v1.0
An AI voice changer harnessing the power of OpenAI and VoiceVox for seamless voice transformation.

## Purpose
WhisperingNova is an extraordinary project that aims to revolutionize voice modulation. It offers a unique and immersive experience by enabling users to effortlessly transform their voices into captivating anime-style renditions

## Technologies Used
- Python    (Programming Language)
- Docker    (Container Service)
- Whisper AI    (SPEECH to TEXT Engine)
- GPT3.5  (Translates English Text to Japanese Text)
- VoiceVox  (TEXT to SPEECH Engine) (For Japanese Output)
- Markdown  (Web Markup Language)
- Git   (Version Control System)

## Applicability
WhisperingNova falls under the category of Entertainment/Arts, offering a unique and immersive voice transformation experience. Whether you are an aspiring VTuber, an anime enthusiast, or a gamer. WhisperingNova usage is simply a Voice Tranformation Service under fair usage.

## How to install
Head over to the [releases](https://github.com/NONAN23x/WhisperingNova/releases) section

## How it works
- This python program will attempt to record your mic for 5 seconds (this is hardcoded for now)
- The recorded audio is then saved to a .wav file
- Then the audio file is sent to OpenAI's Whisper AI to generate a English Transcript of our audio
- English transcript received transcript is sent to OpenAI's GPT 3.5 for translation
- The translated text is then fed to the VoiceVox engine, which is a docker service.
- Resultant audio is stored in another text file and then played

## Bugs and Issues
Please report your findings at [issues](https://github.com/NONAN23x/WhisperingNova/issues)
