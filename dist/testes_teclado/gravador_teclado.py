import csv
from pynput import keyboard
from datetime import datetime

# Nome do arquivo CSV que será gerado pelo script
NOME_ARQUIVO = 'teclas_gravadas.csv'

# Cria o arquivo e adiciona o cabeçalho se ele não existir
try:
    with open(NOME_ARQUIVO, mode='x', newline='', encoding='utf-8') as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(['Data e Hora', 'Tecla'])
except FileExistsError:
    pass

def ao_pressionar(tecla):
    try:
        # Captura o caractere normal (letras, números)
        caractere = tecla.char if tecla.char is not None else str(tecla)
    except AttributeError:
        # Captura chaves especiais (Espaço, Enter, etc.)
        caractere = str(tecla)
    
    agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    # Salva no arquivo CSV
    with open(NOME_ARQUIVO, mode='a', newline='', encoding='utf-8') as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow([agora, caractere])

def ao_soltar(tecla):
    # Pressione a tecla ESC para encerrar a gravação
    if tecla == keyboard.Key.esc:
        print(f"\nGravação encerrada. Os dados foram salvos em '{NOME_ARQUIVO}'.")
        return False

print("Gravando teclas... Pressione 'ESC' a qualquer momento para parar.")

# Inicia o monitoramento do teclado
with keyboard.Listener(on_press=ao_pressionar, on_release=ao_soltar) as listener:
    listener.join()
