import pyodbc

# Ajuste os dados abaixo
SERVER = "N001045"
DATABASE = "discord_loot"
USERNAME = "sa"
PASSWORD = "Mxf@2026"

try:
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD}"
    )

    cursor = conn.cursor()

    # INSERT de teste
    cursor.execute("""
        INSERT INTO drops (
            discord_message_id,
            data_hora,
            item
        )
        VALUES (?, GETDATE(), ?)
    """, 999999999, "TESTE PYTHON")

    conn.commit()

    print("✅ Registro gravado com sucesso!")

    # Verificar se gravou
    cursor.execute("""
        SELECT TOP 1 *
        FROM drops
        WHERE discord_message_id = ?
    """, 999999999)

    resultado = cursor.fetchone()

    if resultado:
        print("✅ Registro encontrado:")
        print(resultado)
    else:
        print("❌ Registro não encontrado.")

except Exception as e:
    print("Erro:", e)

finally:
    if 'conn' in locals():
        conn.close()