import cv2
import pytesseract
import numpy as np
import time
import csv
import os
from PIL import ImageGrab

# Caminho do Tesseract no Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# =========================================================================
# 🎯 COORDENADAS: Use o rastreador de mouse para focar na área do dano.
# Evite usar números maiores que sua tela real (1536x960) para não travar.
# =========================================================================
COORDENADAS_CAPTURA = (618, 380, 918, 580) # Centro da tela (Dano)
NOME_ARQUIVO = "historico_cabal_realtime.csv"

# Variáveis para evitar ler o mesmo número várias vezes seguidas
ultimo_valor_lido = None
tempo_ultimo_dano = time.time()

def processar_imagem(imagem_pil):
    cap_np = np.array(imagem_pil)
    cinza = cv2.cvtColor(cap_np, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(cinza, 127, 255, cv2.THRESH_BINARY_INV)
    return threshold

def salvar_valor_instantaneo(valor):
    """Grava o número de dano no arquivo CSV estruturado para o Excel."""
    arquivo_existe = os.path.exists(NOME_ARQUIVO)
    with open(NOME_ARQUIVO, mode='a', newline='', encoding='utf-8') as arquivo:
        escritor = csv.writer(arquivo, delimiter=';')
        
        # Cria as colunas caso o arquivo seja novo ou esteja zerado
        if not arquivo_existe or os.stat(NOME_ARQUIVO).st_size == 0:
            escritor.writerow(["Data_Hora", "Valor_Capturado"])
            
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        escritor.writerow([timestamp, valor])

print("=== MONITOR DE ESTATÍSTICAS CABAL (SALVAMENTO SEGURO) ===")
print(f"[+] Gravando automaticamente em tempo real em: {os.path.abspath(NOME_ARQUIVO)}")
print("[!] Pressione a tecla 'Q' na janela gráfica para fechar o programa.\n")

try:
    while True:
        # 1. Captura a imagem da tela
        print_tela = ImageGrab.grab(bbox=COORDENADAS_CAPTURA)
        frame = cv2.cvtColor(np.array(print_tela), cv2.COLOR_RGB2BGR)
        
        # 2. Prepara a imagem para o Tesseract
        imagem_tratada = processar_imagem(print_tela)
        
        # 3. O OCR lê os números
        config_ocr = '--psm 6 -c tessedit_char_whitelist=0123456789'
        resultado_texto = pytesseract.image_to_string(imagem_tratada, config=config_ocr).strip()
        
        # Filtra apenas os dígitos
        texto_limpo = "".join([c for c in resultado_texto if c.isdigit()])
        
        # 4. Processa e Salva a Estatística
        if texto_limpo:
            valor_final = int(texto_limpo)
            tempo_atual = time.time()
            
            # Só grava se for um número inédito OU se o último dano já sumiu da tela (passou mais de 0.8s)
            if valor_final != ultimo_valor_lido or (tempo_atual - tempo_ultimo_dano > 0.8):
                salvar_valor_instantaneo(valor_final)
                print(f"[🎯] Gravado no CSV: {valor_final}")
                
                ultimo_valor_lido = valor_final
                tempo_ultimo_dano = tempo_atual
            
            # Texto verde na janela se gravou/leu
            cv2.putText(frame, f"Lido: {valor_final}", (10, 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        else:
            # Se a tela ficar vazia por mais de meio segundo, limpa a memória do último valor
            if time.time() - tempo_ultimo_dano > 0.5:
                ultimo_valor_lido = None
                
            cv2.putText(frame, "Procurando numeros...", (10, 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        # Desenha a borda vermelha ao redor do quadrado monitorado
        cv2.rectangle(frame, (0, 0), (frame.shape[1]-1, frame.shape[0]-1), (0, 0, 255), 2)
        
        # Exibe a janela gráfica com as marcações na tela
        cv2.imshow("Monitor de Captura - Teste", frame)
        
        # Mantém a janela atualizada e checa fechamento com 'Q'
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\n[-] Programa encerrado.")
finally:
    cv2.destroyAllWindows()
