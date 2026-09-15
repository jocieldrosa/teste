import pyautogui
import time

print("Você tem 7 segundos para abrir a tela...")
time.sleep(7)

posicao = pyautogui.locateCenterOnScreen(
    'templates/pet.png',
    confidence=0.8
)

if posicao:
    print(f"Imagem encontrada em X={posicao.x}, Y={posicao.y}")
else:
    print("Imagem não encontrada")