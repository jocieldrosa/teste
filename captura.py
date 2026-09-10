import time
import random
import pydirectinput  # Biblioteca correta para jogos DirectX
from pynput import keyboard  # Usada apenas para monitorar a ativação

# Configurações globais
MACRO_ATIVO = False
TECLA_ATIVACAO = keyboard.Key.f4

def executar_macro():
    global MACRO_ATIVO
    print("Macro Iniciado! Alterne para a janela do Cabal.")
    
    while MACRO_ATIVO:
        # 1. Seleciona o monstro mais próximo (Tecla padrão Z)
        pydirectinput.press('z')
        time.sleep(random.uniform(0.1, 0.15)) # Pequeno atraso humano
        
        # 2. Executa a sequência de Skills (Exemplo: Hotbar 1, 2 e 3)
        for skill in ['1', '2', '3']:
            if not MACRO_ATIVO: 
                break
            pydirectinput.press(skill)
            # Atraso simulando o tempo de animação/cooldown da skill
            time.sleep(random.uniform(0.6, 0.8)) 

def ao_pressionar(tecla):
    global MACRO_ATIVO
    if tecla == TECLA_ATIVACAO:
        MACRO_ATIVO = not MACRO_ATIVO
        if MACRO_ATIVO:
            # Executa o macro em loop
            executar_macro()
        else:
            print("Macro Pausado.")

# Inicia o monitor de teclas em segundo plano
with keyboard.Listener(on_press=ao_pressionar) as listener:
    listener.join()
