import pyaudio
import wave
import keyboard

def record_audio(filename):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100

    audio = pyaudio.PyAudio()

    stream = audio.open(format=format, channels=channels,
                        rate=rate, input=True,
                        frames_per_buffer=chunk)

    print("Recording started... Press 'S' to stop recording.")

    frames = []

    # Start recording when 'S' key is pressed
    keyboard.wait('s')

    while True:
        # Read audio data in chunks
        data = stream.read(chunk)
        frames.append(data)

        # Stop recording when 'S' key is released
        if keyboard.is_pressed('s') == False:
            break

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

# Specify the filename for the recording
filename = 'recorded_audio.wav'

# Call the record_audio function
record_audio(filename)
