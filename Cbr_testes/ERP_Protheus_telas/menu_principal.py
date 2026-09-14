import cv2
import mss
import numpy as np
import pyautogui
import time
from pathlib import Path

# ==========================
# CONFIGURAÇÕES
# ==========================

THRESHOLD = 0.20
TEMPO_ENTRE_TENTATIVAS = 0.3
TEMPO_APOS_CLIQUE = 3
TIMEOUT_ETAPA = 30

# ==========================
# FLUXO
# ==========================

FLUXO_BOTOES = [
    "atualizacao.png",
    "cadastros.png"
]

# ==========================
# CACHE DOS TEMPLATES
# ==========================

templates = {}

for arquivo in FLUXO_BOTOES:

    caminho = Path("templates") / arquivo

    img = cv2.imread(
        str(caminho),
        cv2.IMREAD_GRAYSCALE
    )

    if img is None:
        print(f"Erro carregando {arquivo}")
        exit()

    templates[arquivo] = img

# ==========================
# MSS
# ==========================

sct = mss.mss()
monitor = sct.monitors[1]

# ==========================
# LOCALIZAR E CLICAR
# ==========================

def procurar_e_clicar(nome_template):

    screenshot = sct.grab(monitor)

    tela = np.array(screenshot)

    tela_gray = cv2.cvtColor(
        tela,
        cv2.COLOR_BGRA2GRAY
    )

    template = templates[nome_template]

    resultado = cv2.matchTemplate(
        tela_gray,
        template,
        cv2.TM_CCOEFF_NORMED
    )

    _, max_val, _, max_loc = cv2.minMaxLoc(
        resultado
    )

    print(
        f"🔍 {nome_template} | "
        f"Confiança: {max_val:.4f}"
    )

    if max_val < THRESHOLD:
        return False

    h, w = template.shape

    centro_x = max_loc[0] + w // 2
    centro_y = max_loc[1] + h // 2

    print(
        f"✅ Encontrado em "
        f"({centro_x},{centro_y})"
    )

    pyautogui.click(
        centro_x,
        centro_y
    )

    return True

# ==========================
# EXECUÇÃO
# ==========================

print("🚀 Iniciando em 5 segundos...")
time.sleep(5)

for botao in FLUXO_BOTOES:

    print("\n" + "=" * 50)
    print(f"ETAPA: {botao}")
    print("=" * 50)

    inicio = time.time()

    while True:

        if procurar_e_clicar(botao):
            break

        if (
            time.time() - inicio
            > TIMEOUT_ETAPA
        ):

            print(
                f"⏰ Timeout em {botao}"
            )

            exit()

        time.sleep(
            TEMPO_ENTRE_TENTATIVAS
        )

    time.sleep(
        TEMPO_APOS_CLIQUE
    )

print("\n🎉 Fluxo concluído")