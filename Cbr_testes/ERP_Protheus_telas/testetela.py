import cv2
import numpy as np
from PIL import ImageGrab

tela = ImageGrab.grab(all_screens=True)
tela = cv2.cvtColor(np.array(tela), cv2.COLOR_RGB2BGR)

template = cv2.imread("templates/entrar_ok.png")

h, w = template.shape[:2]

resultado = cv2.matchTemplate(
    tela,
    template,
    cv2.TM_CCOEFF_NORMED
)

_, confianca, _, posicao = cv2.minMaxLoc(resultado)

print("Confiança:", confianca)
print("Posição:", posicao)

x1, y1 = posicao
x2, y2 = x1 + w, y1 + h

cv2.rectangle(
    tela,
    (x1, y1),
    (x2, y2),
    (0, 255, 0),
    5
)

cv2.imwrite("resultado.png", tela)

print("resultado.png gerado")