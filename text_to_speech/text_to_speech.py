from gtts import gTTS
import pygame
import os
import threading

def play(text, lang="pt-br"):
    # Generate speech with gTTS
    tts = gTTS(text, lang=lang)
    tts.save("output.mp3")
    
    # Play the audio using Pygame
    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pass

def text_to_speech(text, lang="pt-BR"):
    """Gera e toca áudio usando threads."""
    # Gerar o áudio (exemplo com eSpeak ou PicoTTS)
    # Criar e iniciar a thread para reproduzir o áudio
    audio_thread = threading.Thread(target=play, args=(text,))
    audio_thread.start()
