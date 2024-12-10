from gtts import gTTS
import pygame
import os
import threading
import states.config as config

output_number = 0

def play(text, lang="pt-br"):
    global output_number
    # Generate speech with gTTS
    tts = gTTS(text, lang=lang)
    tts.save(f"text_to_speech/output/output{output_number}.mp3")
    
    # Play the audio using Pygame
    output_sound = pygame.mixer.Sound(f"text_to_speech/output/output{output_number}.mp3")
    output_number += 1
    config.channel1.play(output_sound)
    config.channel1.set_volume(0.0, 1.0)


def text_to_speech(text, lang="pt-BR"):
    """Gera e toca áudio usando threads."""
    # Gerar o áudio (exemplo com eSpeak ou PicoTTS)
    # Criar e iniciar a thread para reproduzir o áudio
    audio_thread = threading.Thread(target=play, args=(text,))
    audio_thread.start()
