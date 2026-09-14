import cv2
import mss
import numpy as np
import pyautogui
import time

# ==========================
# CONFIGURAÇÕES
# ==========================
TEMPLATE = "templates/atualizacao.png"
THRESHOLD = 0.90

# Pequena pausa para segurança
time.sleep(2)

print("Capturando tela...")

# ==========================
# CAPTURA DE TELA
# ==========================
with mss.mss() as sct:

    monitor = sct.monitors[1]  # monitor principal

    screenshot = sct.grab(monitor)

    tela = np.array(screenshot)

    tela = cv2.cvtColor(tela, cv2.COLOR_BGRA2BGR)

# ==========================
# CARREGA TEMPLATE
# ==========================
template = cv2.imread(TEMPLATE)

if template is None:
    raise FileNotFoundError(
        f"Não foi possível abrir o arquivo: {TEMPLATE}"
    )

# ==========================
# CONVERTE PARA CINZA
# ==========================
tela_gray = cv2.cvtColor(tela, cv2.COLOR_BGR2GRAY)
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

# ==========================
# PROCURA O BOTÃO
# ==========================
resultado = cv2.matchTemplate(
    tela_gray,
    template_gray,
    cv2.TM_CCOEFF_NORMED
)

min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resultado)

print("=" * 50)
print(f"Confiança encontrada: {max_val:.4f}")
print(f"Posição: {max_loc}")
print("=" * 50)

# ==========================
# VALIDA RESULTADO
# ==========================
if max_val >= THRESHOLD:

    h, w = template.shape[:2]

    centro_x = max_loc[0] + w // 2
    centro_y = max_loc[1] + h // 2

    print("✅ Botão encontrado")
    print(f"Centro: ({centro_x}, {centro_y})")

    # desenha retângulo para debug
    cv2.rectangle(
        tela,
        max_loc,
        (max_loc[0] + w, max_loc[1] + h),
        (0, 255, 0),
        2
    )

    cv2.imwrite("resultado.png", tela)

    # move e clica
    pyautogui.moveTo(
        centro_x,
        centro_y,
        duration=0.3
    )

    pyautogui.click()

    print("✅ Clique executado")

else:

    print("❌ Botão não encontrado")
    print(
        f"Confiança insuficiente ({max_val:.4f} < {THRESHOLD})"
    )

    cv2.imwrite("erro_debug.png", tela)