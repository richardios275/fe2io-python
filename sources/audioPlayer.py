import requests
from pydub import AudioSegment
from pydub.playback import play

volume = 70

def change_volume(value):
    global volume
    volume = value

async def download_and_play_audio(url):
    print('bro')
    try:
        # Download the audio file
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Save the audio content to a temporary file
        with open("temp_audio.mp3", "wb") as f:
            f.write(response.content)

        # Load the audio file using pydub
        audio = AudioSegment.from_file("temp_audio.mp3")

        # Volume adjustment

        

        # Play the audio
        play(audio)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")