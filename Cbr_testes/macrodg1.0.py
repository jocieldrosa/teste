from PIL import ImageGrab
import time
import os

PASTA = "capturas"

os.makedirs(PASTA, exist_ok=True)

print("Pressione ENTER para capturar a tela...")
input()

imagem = ImageGrab.grab()

nome = f"{PASTA}/tela_{time.strftime('%Y%m%d_%H%M%S')}.png"
imagem.save(nome)

print(f"Captura salva: {nome}")
