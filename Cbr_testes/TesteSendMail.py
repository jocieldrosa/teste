import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# =========================================================================
# ⚙️ CONFIGURAÇÃO DE TESTE (Mude para os seus dados de e-mail)
# =========================================================================
EMAIL_REMETENTE = "jocieldr@gmail.com"
SENHA_REMETENTE = "huhrazhjpxlxaull"  # Lembre-se: não é a senha normal!
EMAIL_DESTINATARIO = "jociel.rosa@mxfgroup.com.br"
SERVIDOR_SMTP = "gmail.com"
PORTA_SMTP = 587

print("=== INICIANDO TESTE DE DISPARO DE E-MAIL ===")
print(f"[🔄] Tentando conectar ao servidor {SERVIDOR_SMTP}...")

try:
    # 1. Monta a mensagem básica
    msg = MIMEMultipart()
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = EMAIL_DESTINATARIO
    msg['Subject'] = "Teste de Conexão Python - Macro Cabal"
    
    corpo = "Olá! Se você recebeu este e-mail, a autenticação SMTP do seu script Python está funcionando perfeitamente!"
    msg.attach(MIMEText(corpo, 'plain'))
    
    # 2. Conecta ao servidor e tenta autenticar
    server = smtplib.SMTP(SERVIDOR_SMTP, PORTA_SMTP)
    server.starttls()  # Ativa a criptografia de segurança
    
    print("[🔄] Servidor respondendo. Tentando fazer login...")
    server.login(EMAIL_REMETENTE, SENHA_REMETENTE)
    
    print("[🔄] Login efetuado! Enviando mensagem...")
    server.sendmail(EMAIL_REMETENTE, EMAIL_DESTINATARIO, msg.as_string())
    server.quit()
    
    print("\n[✓] SUCESSO TOTAL! O e-mail foi enviado. Verifique a caixa de entrada (ou spam) do destinatário.")

except smtplib.SMTPAuthenticationError:
    print("\n[❌ ERRO DE AUTENTICAÇÃO]: O e-mail ou a senha de aplicativo estão incorretos.")
    print("👉 Se você usa o Gmail, certifique-se de ter gerado uma 'Senha de App' nas configurações da Conta Google.")
    
except Exception as e:
    print(f"\n[❌ ERRO DESCONHECIDO]: {e}")