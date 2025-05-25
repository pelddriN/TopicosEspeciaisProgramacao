import os
import tkinter as tk
from tkinter import filedialog, scrolledtext
from groq import Groq
from tkinter import ttk
import pygame
import time
import threading

# Inicializa o cliente Groq
client = Groq()

# Inicializa o pygame para reprodução de áudio
pygame.mixer.init()

audio_filename = ""
transcription_data = []

def selecionar_arquivo():
    global audio_filename
    audio_filename = filedialog.askopenfilename(filetypes=[("Arquivos de áudio", "*.mp3;*.wav;*.m4a")])
    if audio_filename:
        transcrever_audio(audio_filename)

def transcrever_audio(filename):
    global transcription_data
    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(filename, file.read()),
            model="whisper-large-v3-turbo",
            prompt="Anúncio",
            response_format="json",
            language="pt",
            temperature=0.0
        )
        if hasattr(transcription, "words"):
            transcription_data = transcription.words  # Obtém as palavras com timestamps
        else:
            transcription_data = []
        exibir_transcricao(transcription.text)

def exibir_transcricao(texto):
    texto_transcricao.config(state=tk.NORMAL)
    texto_transcricao.delete(1.0, tk.END)
    texto_transcricao.insert(tk.END, texto)
    texto_transcricao.config(state=tk.DISABLED)

def limpar_transcricao():
    texto_transcricao.config(state=tk.NORMAL)
    texto_transcricao.delete(1.0, tk.END)
    texto_transcricao.config(state=tk.DISABLED)

def reproduzir_audio():
    if audio_filename:
        pygame.mixer.music.load(audio_filename)
        pygame.mixer.music.play()
        threading.Thread(target=sincronizar_transcricao, daemon=True).start()

def parar_audio():
    pygame.mixer.music.stop()

def sincronizar_transcricao():
    if not transcription_data:
        return
    
    start_time = time.time()
    texto_transcricao.config(state=tk.NORMAL)
    texto_transcricao.delete(1.0, tk.END)
    texto_transcricao.tag_config("highlight", foreground="blue")
    
    full_text = " "
    for word in transcription_data:
        full_text += word.text + " "
    texto_transcricao.insert(tk.END, full_text)
    
    for word in transcription_data:
        start, end, text = word.start, word.end, word.text
        while time.time() - start_time < start:
            time.sleep(0.1)
        
        texto_transcricao.tag_remove("highlight", "1.0", tk.END)
        index = texto_transcricao.search(text, "1.0", tk.END)
        if index:
            end_index = f"{index}+{len(text)}c"
            texto_transcricao.tag_add("highlight", index, end_index)
        
        while time.time() - start_time < end:
            time.sleep(0.1)
    
    texto_transcricao.config(state=tk.DISABLED)

# Configuração da GUI
root = tk.Tk()
root.title("Transcrição de Áudio")
root.geometry("700x500")
root.configure(bg="#f0f0f0")

frame_top = tk.Frame(root, bg="#0078D7", height=50)
frame_top.pack(fill=tk.X)

label_titulo = tk.Label(frame_top, text="Transcrição de Áudio", bg="#0078D7", fg="white", font=("Arial", 16, "bold"))
label_titulo.pack(pady=10)

frame_buttons = tk.Frame(root, bg="#f0f0f0")
frame_buttons.pack(pady=10)

btn_selecionar = ttk.Button(frame_buttons, text="Selecionar Arquivo de Áudio", command=selecionar_arquivo)
btn_selecionar.grid(row=0, column=0, padx=10, pady=5)

btn_reproduzir = ttk.Button(frame_buttons, text="Reproduzir Áudio", command=reproduzir_audio)
btn_reproduzir.grid(row=0, column=1, padx=10, pady=5)

btn_parar = ttk.Button(frame_buttons, text="Parar Áudio", command=parar_audio)
btn_parar.grid(row=0, column=2, padx=10, pady=5)

btn_limpar = ttk.Button(frame_buttons, text="Limpar", command=limpar_transcricao)
btn_limpar.grid(row=0, column=3, padx=10, pady=5)

texto_transcricao = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20, state=tk.DISABLED, font=("Arial", 12))
texto_transcricao.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

root.mainloop()
