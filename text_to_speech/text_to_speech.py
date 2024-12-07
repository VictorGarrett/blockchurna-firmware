from gtts import gTTS
import pygame
import os
import threading

output_number = 0

def play(text, lang="pt-br"):
    global output_number
    # Generate speech with gTTS
    tts = gTTS(text, lang=lang)
    tts.save(f"text_to_speech/output/output{output_number}.mp3")
    
    # Play the audio using Pygame
    pygame.mixer.init()
    pygame.mixer.music.load(f"text_to_speech/output/output{output_number}.mp3")
    output_number += 1
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pass

def text_to_speech(text, lang="pt-BR"):
    """Gera e toca áudio usando threads."""
    # Gerar o áudio (exemplo com eSpeak ou PicoTTS)
    # Criar e iniciar a thread para reproduzir o áudio
    audio_thread = threading.Thread(target=play, args=(text,))
    audio_thread.start()
