import requests
import os
import time

# =========================================================================
# ⚙️ CONFIGURAÇÃO DE TESTE: Cole o link que você copiou do seu Discord aqui
# =========================================================================
URL_WEBHOOK = "https://discordapp.com/api/webhooks/1547328533678788669/tDYZ5WN7r3nN1o7OnOnJFZZwB3vCkcpEr2enW0yH90A8BPfovv4sRfLVztiDBtXgNXeZ"

# Vamos criar um arquivo de texto bobo só para fingir que é o seu arquivo do jogo
NOME_ARQUIVO_TESTE = "teste_macro.txt"
with open(NOME_ARQUIVO_TESTE, "w", encoding="utf-8") as f:
    f.write(f"Teste de envio realizado com sucesso em: {time.strftime('%d/%m/%Y %H:%M:%S')}")

print("=== INICIANDO TESTE VIA WEBHOOK DISCORD ===")
print("[🔄] Tentando enviar o arquivo para o seu canal do Discord...")

try:
    # Prepara a mensagem de texto estruturada
    payload = {
        "content": f"🚀 **[NOTIFICAÇÃO DE MACRO]** Teste de envio de arquivos executado em: {time.strftime('%H:%M:%S')}!"
    }
    
    # Abre o arquivo local e prepara para o upload
    with open(NOME_ARQUIVO_TESTE, "rb") as arquivo:
        arquivos_upload = {
            "file": (os.path.basename(NOME_ARQUIVO_TESTE), arquivo)
        }
        
        # Dispara a requisição HTTP para os servidores do Discord
        resposta = requests.post(URL_WEBHOOK, data=payload, files=arquivos_upload)
        
    # Limpa o arquivo de teste do computador
    if os.path.exists(NOME_ARQUIVO_TESTE):
        os.remove(NOME_ARQUIVO_TESTE)

    # Verifica se o Discord aceitou o envio (Código HTTP 200 ou 204 significa sucesso)
    if resposta.status_code in [200, 204]:
        
        print("\n[✓] SUCESSO TOTAL! Olhe o canal de texto do seu Discord, o arquivo já está lá.")
    else:
        print(f"\n[❌ ERRO NO DISCORD]: O servidor recusou o envio. Código de resposta: {resposta.status_code}")

except Exception as e:
    print(f"\n[❌ ERRO DE CONEXÃO]: Não foi possível alcançar o Discord. Detalhes: {e}")
