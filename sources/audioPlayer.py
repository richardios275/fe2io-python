import requests
import pygame
from datetime import datetime
from pygame import mixer_music
from urllib.parse import urlparse

volume = 70
deathVolume = False
fadein = True

audio_cache = {}
filename = ""

VERY_BIG_NUMBER = 2147483647

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
    #Variables
    current_time = datetime.now()
    download_failed = False

    # Stop current audio from playing
    mixer_music.unload()
    mixer_music.stop()

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
            download_failed = True
            print(f"Error: {e}")

    #Play music
    if download_failed != True:
        elapsed_time = int((datetime.now() - current_time).total_seconds())
        mixer_music.load(filename)
        mixer_music.play(VERY_BIG_NUMBER, elapsed_time, 1000)    

pygame.mixer.init()
set_volume(volume)