import pyodbc

try:
    conexao = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=teste;"
        "UID=sa;"
        "PWD=Mxf@2026;"
    )

    print("Conectado!")

except pyodbc.Error as erro:
    print("Erro:", erro)
    