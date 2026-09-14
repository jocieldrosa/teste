import cv2
import numpy as np
import time
import csv
import os
import keyboard

from PIL import ImageGrab

# ==========================
# CONFIGURAÇÕES
# ==========================

ARQUIVO_CSV = "estatisticas_cabal.csv"

# Ajuste esta região
REGIAO_MONITORADA = (900, 500, 1500, 900)

# Templates
TEMPLATE_UIP = "templates/tela_menor.png"
TEMPLATE_CLEAR = "templates/tela1.png"

# Sensibilidade
LIMIAR_DETECCAO = 0.80

# Controle
monitorando = False

# Cooldowns
cooldown_uip = 0
cooldown_clear = 0


# ==========================
# SALVAR CSV
# ==========================

def registrar_evento(evento, valor):

    arquivo_existe = os.path.exists(ARQUIVO_CSV)

    with open(
        ARQUIVO_CSV,
        "a",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        escritor = csv.writer(
            arquivo,
            delimiter=";"
        )

        if not arquivo_existe:

            escritor.writerow([
                "DataHora",
                "Evento",
                "Valor"
            ])

        escritor.writerow([
            time.strftime("%Y-%m-%d %H:%M:%S"),
            evento,
            valor
        ])


# ==========================
# TEMPLATE MATCH
# ==========================

def detectar_template(frame, template_path):

    if not os.path.exists(template_path):

        return False, 0

    template = cv2.imread(template_path)

    if template is None:

        return False, 0

    resultado = cv2.matchTemplate(
        frame,
        template,
        cv2.TM_CCOEFF_NORMED
    )

    _, max_val, _, _ = cv2.minMaxLoc(resultado)

    return max_val >= LIMIAR_DETECCAO, max_val


# ==========================
# INÍCIO
# ==========================

print("\n=== MONITOR CABAL ===")
print("F8  = Iniciar")
print("F9  = Pausar")
print("F10 = Encerrar")
print()

try:

    while True:

        # ------------------
        # ATALHOS
        # ------------------

        if keyboard.is_pressed("f8"):

            monitorando = True

            print("[START] Monitoramento iniciado")

            time.sleep(0.5)

        if keyboard.is_pressed("f9"):

            monitorando = False

            print("[PAUSE] Monitoramento pausado")

            time.sleep(0.5)

        if keyboard.is_pressed("f10"):

            print("[EXIT] Encerrando programa")

            break

        # ------------------
        # PAUSADO
        # ------------------

        if not monitorando:

            time.sleep(0.1)

            continue

        # ------------------
        # CAPTURA
        # ------------------

        captura = ImageGrab.grab(
            bbox=REGIAO_MONITORADA
            
                     
        )
        
        captura.save("teste123.png")
        print("Captura salva como 'captura.png'")   
        
        registrar_evento( "UIP", "1" )
        
        registrar_evento( "FIM DG", "DG" )
        
        captura.save("area_monitorada.png")

        frame = cv2.cvtColor(
            np.array(captura),
            cv2.COLOR_RGB2BGR
        )

        agora = time.time()

        # ------------------
        # UIP
        # ------------------

        encontrou_uip, score_uip = detectar_template(
            frame,
            TEMPLATE_UIP
        )

        if encontrou_uip:

            if agora - cooldown_uip > 5:

                registrar_evento(
                    "UIP",
                    "1"
                )

                print(
                    f"[UIP DETECTADO] Score={score_uip:.2f}"
                )

                cooldown_uip = agora

        # ------------------
        # DG CLEAR
        # ------------------

        encontrou_clear, score_clear = detectar_template(
            frame,
            TEMPLATE_CLEAR
        )

        if encontrou_clear:

            if agora - cooldown_clear > 30:

                registrar_evento(
                    "FIM_DG",
                    "DG"
                )

                print(
                    f"[DG FINALIZADA] Score={score_clear:.2f}"
                )

                cooldown_clear = agora

        # ------------------
        # INFORMAÇÕES TELA
        # ------------------

        cv2.putText(
            frame,
            f"UIP: {score_uip:.2f}",
            (10, 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"CLEAR: {score_clear:.2f}",
            (10, 55),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 0),
            2
        )

        cv2.putText(
            frame,
            "F8=START  F9=PAUSE  F10=EXIT",
            (10, 85),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 255),
            1
        )

        cv2.imshow(
            "Monitor Cabal",
            frame
        )

        cv2.waitKey(1)

except KeyboardInterrupt:

    print("\nInterrompido pelo usuário")

finally:

    cv2.destroyAllWindows()

    print("Programa finalizado")