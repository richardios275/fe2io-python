import os
import json
import requests
import pygame
import tempfile
from datetime import datetime
from pygame import mixer_music
from pydub import AudioSegment
from urllib.parse import urlparse

# Constants
VERY_BIG_NUMBER = 2147483647

# Options
volume = 70
deathVolume = False
fadein = True

# Audio Stuff
unsupported_formats = {"m4a"}
audio_cache = {}
filename = ""
audio_folder = "fe2io_files"
cache_file = os.path.join(audio_folder, "audio_cache.json")

# Load audio cache from the JSON file if it exists, otherwise create an empty dictionary
try:
    with open(cache_file, "r") as json_file:
        audio_cache = json.load(json_file)
except FileNotFoundError:
    audio_cache = {}
        
def toggle_death_volume(enum):
    global deathVolume
    if enum == 1:
        deathVolume = True
        set_volume(volume)
    elif enum == 2:
        mixer_music.stop()

def toggle_leave():
    mixer_music.stop()

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

def convert_audio(file_path, output_dir):
    audio = AudioSegment.from_file(file_path)
    audio.export(output_dir, format='mp3')

def set_audio(url='https://github.com/anars/blank-audio/blob/master/250-milliseconds-of-silence.mp3', utc_time=0):
    #Variables
    current_time = datetime.now()
    download_failed = False

    # Stop current audio from playing
    mixer_music.unload()
    mixer_music.stop()

    toggle_death_volume(False)
    
    # Fix error if URL is empty
    if len(url) < 1:
        url = 'https://github.com/anars/blank-audio/blob/master/250-milliseconds-of-silence.mp3'

    # Load audio from cache if available, download if not.
    if url in audio_cache:
        filename = audio_cache[url]
    else:
        try:
            # Download the audio file
            response = requests.get(url)
            response.raise_for_status()

            # Get the file extension of the audio
            ext = get_file_extension(url)

            # Convert the file to mp3 if it downloads an unsupported file format
            if ext in unsupported_formats:
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as temp_file:
                    temp_file.write(response.content)
                convert_audio(temp_file.name, os.path.join(audio_folder, f"{len(audio_cache)}.mp3"))
                filename = os.path.join(audio_folder, f"{len(audio_cache)}.mp3")
            else:
                filename = os.path.join(audio_folder, f"{len(audio_cache)}.{ext}")
                with open(filename, "wb") as f:
                    f.write(response.content)
            
            # Save audio to cache
            audio_cache[url] = filename 

            # Update json file
            with open(cache_file, "w") as json_file:
                json.dump(audio_cache, json_file)

        except requests.exceptions.RequestException as e:
            download_failed = True
            print(f"Error: {e}")
            set_audio()

    #Play music
    #If utc_time is present, then it'll wait until utc_time 
    if download_failed != True:
        mixer_music.load(filename)

        if utc_time == 0:
            elapsed_time = (datetime.now() - current_time).total_seconds()
            mixer_music.play(VERY_BIG_NUMBER, elapsed_time, 1000 if fadein else 0)
        else:
            current_start_utc_time = datetime.utcnow().timestamp()
            playing_time = (utc_time - current_start_utc_time) / 1000
            mixer_music.play(VERY_BIG_NUMBER, playing_time, 1000 if fadein else 0)  

pygame.mixer.init()
set_volume(volume)