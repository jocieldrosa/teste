import cv2
import numpy as np
import time
import os
import requests 
import ctypes 
from PIL import ImageGrab
import pynput

# Desativa a escala de tela do Windows para coletar os pixels corretos (1536x960)
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    ctypes.windll.user32.SetProcessDPIAware()

# Configuração de pastas
PASTA_FLUXO = "fluxo_inicializacao_cabal"

# =========================================================================
# ⚙️ CONFIGURAÇÃO DO DISCORD: Cole o link completo do seu Webhook aqui
# =========================================================================
URL_WEBHOOK = "https://discordapp.com/api/webhooks/1547328533678788669/tDYZ5WN7r3nN1o7OnOnJFZZwB3vCkcpEr2enW0yH90A8BPfovv4sRfLVztiDBtXgNXeZ"

# Atalhos do Teclado
TECLA_START = pynput.keyboard.Key.f9
TECLA_STOP = pynput.keyboard.Key.f10

MONITORAMENTO_ATIVO = False
SCRIPT_RODANDO = True
ultimo_frame_cinza = None
contador_print = 1

if not os.path.exists(PASTA_FLUXO):
    os.makedirs(PASTA_FLUXO)

def enviar_imagem_instantanea(caminho_foto, mensagem_texto):
    """Envia a imagem imediatamente para o Discord de forma isolada."""
    try:
        payload = {"content": mensagem_texto}
        with open(caminho_foto, "rb") as anexo:
            arquivos_upload = {"file": (os.path.basename(caminho_foto), anexo)}
            # Dispara para o Webhook
            resposta = requests.post(URL_WEBHOOK, data=payload, files=arquivos_upload)
            
        if resposta.status_code in [200, 204]:
            print(f"[✓] Enviada para o Discord com sucesso!")
        else:
            print(f"[❌] Falha ao enviar para o Discord. Código HTTP: {resposta.status_code}")
    except Exception as e:
        print(f"[⚠️ Erro de rede]: {e}")

def verificar_mudanca_tela():
    global ultimo_frame_cinza, contador_print
    if not MONITORAMENTO_ATIVO:
        return
        
    try:
        print_tela = ImageGrab.grab()
        frame = cv2.cvtColor(np.array(print_tela), cv2.COLOR_RGB2BGR)
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cinza_pequeno = cv2.resize(cinza, (300, 200))
        
        if ultimo_frame_cinza is None:
            ultimo_frame_cinza = cinza_pequeno
            return
            
        diferenca = cv2.absdiff(ultimo_frame_cinza, cinza_pequeno)
        pontuacao_mudanca = np.sum(diferenca) / float(cinza_pequeno.size)
        
        if pontuacao_mudanca > 15.0:  
            timestamp = time.strftime("%H%M%S")
            # 🟢 OTIMIZAÇÃO: Salvando em JPG com 70% de qualidade para ficar ultra leve
            nome_arquivo = f"{PASTA_FLUXO}/tela_{contador_print:02d}_{timestamp}.jpg"
            cv2.imwrite(nome_arquivo, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
            
            print(f"[📺 TELA MUDOU] Processando Print #{contador_print}...")
            
            # Envia em tempo real para o Discord
            enviar_imagem_instantanea(nome_arquivo, f"📺 **[MUDANÇA DE TELA]** Imagem #{contador_print} detectada.")
            
            contador_print += 1
            ultimo_frame_cinza = cinza_pequeno
    except:
        pass

def ao_clicar(x, y, botao, pressionado):
    global contador_print
    if pressionado and MONITORAMENTO_ATIVO:
        try:
            timestamp = time.strftime("%H%M%S")
            print_tela = ImageGrab.grab()
            frame = cv2.cvtColor(np.array(print_tela), cv2.COLOR_RGB2BGR)
            
            alt, larg, _ = frame.shape
            if x < larg and y < alt:
                cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)
            
            # 🟢 OTIMIZAÇÃO: Salvando em JPG compactado
            nome_arquivo = f"{PASTA_FLUXO}/clique_{contador_print:02d}_X{x}_Y{y}_{timestamp}.jpg"
            cv2.imwrite(nome_arquivo, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
            
            print(f"[MIGRANDO CLIQUE] Processando Clique #{contador_print} em X: {x} | Y: {y}...")
            
            # Envia em tempo real para o Discord
            enviar_imagem_instantanea(nome_arquivo, f"🖱️ **[CLIQUE REGISTRADO]** Usuário clicou na coordenada: **X: {x} | Y: {y}**.")
            
            contador_print += 1
        except Exception as e:
            print(f"[⚠️ Erro ao capturar clique]: {e}")

def ao_pressionar_teclado(tecla):
    global MONITORAMENTO_ATIVO, SCRIPT_RODANDO
    if tecla == TECLA_START and not MONITORAMENTO_ATIVO:
        MONITORAMENTO_ATIVO = True
        print("\n[▶️ START] Gravação e Envio em Tempo Real Ativados!")
    elif tecla == TECLA_STOP:
        MONITORAMENTO_ATIVO = False
        SCRIPT_RODANDO = False
        print("\n[⏹️ STOP] Finalizando rotinas de monitoramento.")
        return False

ouvinte_mouse = pynput.mouse.Listener(on_click=ao_clicar)
ouvinte_teclado = pynput.keyboard.Listener(on_press=ao_pressionar_teclado)
ouvinte_mouse.start()
ouvinte_teclado.start()

print("=== MACRO AUDITOR EM TEMPO REAL DISCORD ===")
print("Aperte F9 para START | Aperte F10 para FINALIZAR.\n")

try:
    while SCRIPT_RODANDO:
        verificar_mudanca_tela()
        time.sleep(0.4)
except KeyboardInterrupt:
    print("\n[-] Cancelado.")
finally:
    ouvinte_mouse.stop()
    ouvinte_teclado.stop()