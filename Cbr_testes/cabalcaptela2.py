import cv2
import numpy as np
import time
import os
import shutil  # Para criar o arquivo ZIP
import smtplib # Para enviar o e-mail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from PIL import ImageGrab
import pynput

# Configurações de pastas e arquivos
PASTA_FLUXO = "fluxo_inicializacao_cabal"
ARQUIVO_ZIP_DESTINO = "fluxo_cabal"  # Irá gerar fluxo_cabal.zip

# =========================================================================
# ⚙️ CONFIGURAÇÃO DE ENVIO DE E-MAIL (Mude para os seus dados)
# NOTA: Para usar o Gmail/Outlook, você precisará de uma "Senha de App"
# =========================================================================
EMAIL_REMETENTE = "jocieldr@gmail.com"
SENHA_REMETENTE = "senha do google"
EMAIL_DESTINATARIO = "jocieldr@gmail.com"
SERVIDOR_SMTP = "://gmail.com"
PORTA_SMTP = 587

TECLA_START = pynput.keyboard.Key.f9
TECLA_STOP = pynput.keyboard.Key.f10

MONITORAMENTO_ATIVO = False
SCRIPT_RODANDO = True
ultimo_frame_cinza = None
contador_print = 1

if not os.path.exists(PASTA_FLUXO):
    os.makedirs(PASTA_FLUXO)

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
    
    # 🟢 CORREÇÃO AQUI: Mudado para 'cinza_pequeno.size' para calcular a média corretamente
    pontuacao_mudanca = np.sum(diferenca) / float(cinza_pequeno.size)
    
    if pontuacao_mudanca > 15.0:  
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"{PASTA_FLUXO}/tela_{contador_print:02d}_{timestamp}.png"
        cv2.imwrite(nome_arquivo, frame)
        print(f"[📺 TELA MUDOU] Print #{contador_print} salvo.")
        contador_print += 1
        ultimo_frame_cinza = cinza_pequeno

def ao_clicar(x, y, botao, pressionado):
    global contador_print
    if pressionado and MONITORAMENTO_ATIVO:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        print_tela = ImageGrab.grab()
        frame = cv2.cvtColor(np.array(print_tela), cv2.COLOR_RGB2BGR)
        cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)
        nome_arquivo = f"{PASTA_FLUXO}/clique_{contador_print:02d}_X{x}_Y{y}_{timestamp}.png"
        cv2.imwrite(nome_arquivo, frame)
        print(f"[🖱️ CLIQUE] X: {x} | Y: {y} -> Print #{contador_print}")
        contador_print += 1

def compactar_e_enviar():
    """Cria um arquivo ZIP da pasta e dispara o envio por e-mail."""
    print("\n[📦] Compactando a pasta de arquivos em formato ZIP...")
    try:
        shutil.make_archive(ARQUIVO_ZIP_DESTINO, 'zip', PASTA_FLUXO)
        arquivo_zip = f"{ARQUIVO_ZIP_DESTINO}.zip"
        print(f"[✓] Arquivo {arquivo_zip} criado com sucesso!")
        
        print("[📧] Preparando disparo do e-mail...")
        msg = MIMEMultipart()
        msg['From'] = EMAIL_REMETENTE
        msg['To'] = EMAIL_DESTINATARIO
        msg['Subject'] = f"Relatório de Macro - Cabal Online ({time.strftime('%d/%m/%Y')})"
        
        corpo_email = "Segue em anexo o arquivo compactado contendo o fluxo de telas e cliques registrados pelo macro."
        msg.attach(MIMEText(corpo_email, 'plain'))
        
        with open(arquivo_zip, "rb") as anexo:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(anexo.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(arquivo_zip)}")
            msg.attach(part)
            
        server = smtplib.SMTP(SERVIDOR_SMTP, PORTA_SMTP)
        server.starttls()
        server.login(EMAIL_REMETENTE, SENHA_REMETENTE)
        server.sendmail(EMAIL_REMETENTE, EMAIL_DESTINATARIO, msg.as_string())
        server.quit()
        print("[✓] E-mail enviado com sucesso!")
        
    except Exception as e:
        print(f"[❌ ERRO NA OPERAÇÃO]: {e}")

def ao_pressionar_teclado(tecla):
    global MONITORAMENTO_ATIVO, SCRIPT_RODANDO
    if tecla == TECLA_START and not MONITORAMENTO_ATIVO:
        MONITORAMENTO_ATIVO = True
        print("\n[▶️ START] Monitoramento ativado!")
    elif tecla == TECLA_STOP:
        MONITORAMENTO_ATIVO = False
        SCRIPT_RODANDO = False
        print("\n[⏹️ STOP] Encerrando gravação...")
        compactar_e_enviar()
        return False

ouvinte_mouse = pynput.mouse.Listener(on_click=ao_clicar)
ouvinte_teclado = pynput.keyboard.Listener(on_press=ao_pressionar_teclado)
ouvinte_mouse.start()
ouvinte_teclado.start()

print("=== MACRO COM LOG AUTOMÁTICO VIA E-MAIL ===")
print("Aperte F9 para COMEÇAR | Aperte F10 para TERMINAR, ZIPAR E ENVIAR.\n")

try:
    while SCRIPT_RODANDO:
        verificar_mudanca_tela()
        time.sleep(0.4)
except KeyboardInterrupt:
    print("\n[-] Cancelado.")
finally:
    ouvinte_mouse.stop()
    ouvinte_teclado.stop()
