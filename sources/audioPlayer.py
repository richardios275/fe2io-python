import requests
import pygame
from pygame import mixer_music
from urllib.parse import urlparse

volume = 70
deathVolume = False
fadein = True

audio_cache = {}
filename = ""

def toggle_death_volume(value):
    global deathVolume
    deathVolume = value
    set_volume(volume)

def toggle_fadein(value):
    global fadein
    fadein = value

def set_volume(vol):
    global volume
    volume = vol
    if deathVolume == True:
        vol = vol / 2
    mixer_music.set_volume(vol / 100)

def get_file_extension(url):
    # Parse the URL to get the path
    path = urlparse(url).path
    # Split the path based on '/'
    parts = path.split('/')
    # Get the last part of the path, which represents the file name
    file_name = parts[-1]
    # Split the file name based on '?' to handle parameters
    file_name_parts = file_name.split('?')
    # Get the first part of the file name, which represents the actual file name
    actual_file_name = file_name_parts[0]
    # Split the actual file name based on '.', and get the last part, which represents the file extension
    extension = actual_file_name.split('.')[-1]
    return extension

def set_audio(url):
    toggle_death_volume(False)

    # Load audio from cache if available, download if not.
    if url in audio_cache:
        filename = audio_cache[url]
    else:
        try:
            if url == None:
                url = 'https://github.com/anars/blank-audio/blob/master/250-milliseconds-of-silence.mp3'
            # Download the audio file
            response = requests.get(url)
            response.raise_for_status()

            # Get the file extension of the audio
            ext = get_file_extension(url)
            filename = f"{len(audio_cache)}.{ext}"
                
            with open(filename, "wb") as f:
                f.write(response.content)

            # Save audio to cache
            audio_cache[url] = filename
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    mixer_music.load(filename)
    mixer_music.play(2, 0.00, 1000)

pygame.init()
set_volume(volume)