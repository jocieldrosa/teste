from PIL import ImageGrab
from pynput import keyboard
import os
import time

PASTA = "capturas"
os.makedirs(PASTA, exist_ok=True)

contador = 1

def ao_pressionar(tecla):
    global contador

    try:
        if tecla == keyboard.Key.f8:

            img = ImageGrab.grab()

            nome = f"{PASTA}/captura_{contador:03d}.png"

            img.save(nome)

            print(f"[✓] Captura salva: {nome}")

            contador += 1

        elif tecla == keyboard.Key.f10:

            print("[X] Encerrando...")
            return False

    except Exception as e:
        print(f"Erro: {e}")

print("=== CAPTURADOR DE TELAS ===")
print("F8  -> Capturar tela")
print("F10 -> Sair")

with keyboard.Listener(on_press=ao_pressionar) as listener:
    listener.join()
