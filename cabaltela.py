import cv2
import numpy as np
import time
import os
from PIL import ImageGrab
import pynput

# Configurações de pastas
PASTA_FLUXO = "fluxo_inicializacao_cabal"
if not os.path.exists(PASTA_FLUXO):
    os.makedirs(PASTA_FLUXO)

# =========================================================================
# ⚙️ ATALHOS CONFIGURADOS:
# F9 -> Inicia o monitoramento de telas e cliques
# F10 -> Para o monitoramento e encerra o script de vez
# =========================================================================
TECLA_START = pynput.keyboard.Key.f9
TECLA_STOP = pynput.keyboard.Key.f10

# Variáveis lógicas de controle
MONITORAMENTO_ATIVO = False
SCRIPT_RODANDO = True

ultimo_frame_cinza = None
contador_print = 1

def verificar_mudanca_tela():
    global ultimo_frame_cinza, contador_print
    if not MONITORAMENTO_ATIVO:
        return
        
    print_tela = ImageGrab.grab()
    frame = cv2.cvtColor(np.array(print_tela), cv2.COLOR_RGB2BGR)
    
    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cinza_pequeno = cv2.resize(cinza, (300, 200))
    
    if ultimo_frame_cinza is None:
        ultimo_frame_cinza = cinza_pequeno
        return
        
    diferenca = cv2.absdiff(ultimo_frame_cinza, cinza_pequeno)
    pontuacao_mudanca = np.sum(diferenca) / float(cinza_pequeno.shape[0] * cinza_pequeno.shape[1])
    
    # Se detectar mudança brusca de tela
    if pontuacao_mudanca > 15.0:  
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"{PASTA_FLUXO}/tela_{contador_print:02d}_{timestamp}.png"
        cv2.imwrite(nome_arquivo, frame)
        print(f"[📺 TELA MUDOU] Print #{contador_print} salvo: {os.path.basename(nome_arquivo)}")
        contador_print += 1
        ultimo_frame_cinza = cinza_pequeno

def ao_clicar(x, y, botao, pressionado):
    global contador_print
    # Só registra o clique se o atalho de START (F9) já tiver sido pressionado
    if pressionado and MONITORAMENTO_ATIVO:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        print_tela = ImageGrab.grab()
        frame = cv2.cvtColor(np.array(print_tela), cv2.COLOR_RGB2BGR)
        
        # Desenha o marcador de clique (bolinha vermelha)
        cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)
        
        nome_arquivo = f"{PASTA_FLUXO}/clique_{contador_print:02d}_X{x}_Y{y}_{timestamp}.png"
        cv2.imwrite(nome_arquivo, frame)
        
        print(f"[🖱️ CLIQUE] Posição registrada em X: {x} | Y: {y} -> Print #{contador_print}")
        contador_print += 1

def ao_pressionar_teclado(tecla):
    global MONITORAMENTO_ATIVO, SCRIPT_RODANDO
    
    # Se apertar F9, liga o rastreador
    if tecla == TECLA_START and not MONITORAMENTO_ATIVO:
        MONITORAMENTO_ATIVO = True
        print("\n[▶️ START] Monitoramento ativado! Pode abrir o jogo e fazer o fluxo.")
        
    # Se apertar F10, desliga tudo e fecha o programa
    elif tecla == TECLA_STOP:
        MONITORAMENTO_ATIVO = False
        SCRIPT_RODANDO = False
        print("\n[⏹️ STOP] Monitoramento encerrado com sucesso. Arquivos salvos!")
        return False  # Para o listener do teclado

# Inicializa os ouvintes em segundo plano
ouvinte_mouse = pynput.mouse.Listener(on_click=ao_clicar)
ouvinte_teclado = pynput.keyboard.Listener(on_press=ao_pressionar_teclado)

ouvinte_mouse.start()
ouvinte_teclado.start()

print("=== RASTREADOR DE FLUXO INTERATIVO (CABAL) ===")
print("Instruções:")
print("1. Deixe o VS Code rodando em segundo plano (como Administrador).")
print("2. Aperte F9 para COMEÇAR o rastreamento.")
print("3. Abra o Cabal e faça seus cliques até entrar no jogo.")
print("4. Aperte F10 para FINALIZAR e fechar o script com segurança.\n")
print("[🔄] Aguardando comando... Pressione F9 para iniciar.")

try:
    while SCRIPT_RODANDO:
        verificar_mudanca_tela()
        time.sleep(0.4)
except KeyboardInterrupt:
    print("\n[-] Forçado encerramento via terminal.")
finally:
    ouvinte_mouse.stop()
    ouvinte_teclado.stop()
