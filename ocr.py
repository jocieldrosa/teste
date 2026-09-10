import pynput
import time
import ctypes

# 🔑 ESTA LINHA CORRIGE OS VALORES MALUCOS:
# Ela força o Windows a reportar os pixels reais do monitor, ignorando o zoom (escala) de 125%/150%
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2) # Para Windows 8.1 / 10 / 11
except:
    ctypes.windll.user32.SetProcessDPIAware() # Alternativa para sistemas mais antigos

def ao_mover(x, y):
    # Mostra a posição X e Y real do pixel na tela
    print(f"Posição Real do Mouse -> X: {x} | Y: {y}      ", end="\r")

print("=== RASTREADOR DE PIXELS EM ALTA PRECISÃO ===")
print("Coloque o mouse no CANTO SUPERIOR ESQUERDO do relógio e anote.")
print("Coloque o mouse no CANTO INFERIOR DIREITO do relógio e anote.")
print("Pressione CTRL + C no terminal do VS Code para fechar.\n")

with pynput.mouse.Listener(on_move=ao_mover) as listener:
    try:
        listener.join()
    except KeyboardInterrupt:
        print("\nRastreamento encerrado.")