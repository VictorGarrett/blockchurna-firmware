from gtts import gTTS
import pygame
import os
import threading
import uuid 
import states.config as config

def generate_audio(text, lang="pt-br"):
    """Gera o áudio com gTTS e retorna o caminho do arquivo salvo."""
    os.makedirs("text_to_speech/output", exist_ok=True)
    filename = f"text_to_speech/output/{uuid.uuid4().hex}.mp3"  # Nome único para evitar conflitos
    tts = gTTS(text, lang=lang)
    tts.save(filename)
    return filename

def play_audio(file_path):
    """Reproduz o áudio usando Pygame."""
    try:
        output_sound = pygame.mixer.Sound(file_path)
        config.channel1.play(output_sound)
        config.channel1.set_volume(0.0, 1.0)

    finally:
        # Remova o arquivo temporário para evitar acúmulo
        if os.path.exists(file_path):
            os.remove(file_path)

def play(text, lang="pt-br"):
    """Combina geração e reprodução de áudio."""
    file_path = generate_audio(text, lang)
    play_audio(file_path)

def text_to_speech(text, lang="pt-BR"):
    """Gera e toca áudio usando threads."""
    audio_thread = threading.Thread(target=play, args=(text, lang))
    audio_thread.start()
