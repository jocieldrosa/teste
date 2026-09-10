import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pyodbc


class ClienteApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Pessoas")
        self.root.geometry("700x500")

        self.conexao = None

        # Botão Conectar
        btn_conectar = tk.Button(
            root,
            text="Conectar Banco",
            command=self.conectar
        )
        btn_conectar.pack(pady=10)

        # Nome
        tk.Label(root, text="Nome").pack()
        self.txt_nome = tk.Entry(root, width=40)
        self.txt_nome.pack()

        # Idade
        tk.Label(root, text="Idade").pack()
        self.txt_idade = tk.Entry(root, width=40)
        self.txt_idade.pack()

        # CPF
        tk.Label(root, text="CPF").pack()
        self.txt_cpf = tk.Entry(root, width=40)
        self.txt_cpf.pack()

        # Botões
        tk.Button(
            root,
            text="Salvar",
            command=self.salvar
        ).pack(pady=5)

        tk.Button(
            root,
            text="Listar Registros",
            command=self.listar
        ).pack(pady=5)

        # Grid
        self.tree = ttk.Treeview(
            root,
            columns=("Codigo", "Nome", "Idade", "CPF"),
            show="headings"
        )

        self.tree.heading("Codigo", text="Código")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Idade", text="Idade")
        self.tree.heading("CPF", text="CPF")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def conectar(self):
        try:
            self.conexao = pyodbc.connect(
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=localhost;"
                "DATABASE=teste;"
                "UID=sa;"
                "PWD=Mxf@2026;"
            )

            messagebox.showinfo(
                "Sucesso",
                "Conectado ao SQL Server!"
            )

        except pyodbc.Error as erro:

            if "18456" in str(erro):
                messagebox.showerror(
                    "Erro",
                    "Usuário ou senha inválidos!"
                )
            else:
                messagebox.showerror(
                    "Erro",
                    str(erro)
                )

    def salvar(self):

        if not self.conexao:
            messagebox.showwarning(
                "Aviso",
                "Conecte ao banco primeiro."
            )
            return

        try:

            cursor = self.conexao.cursor()

            cursor.execute("""
                INSERT INTO cad_nome
                (Nome, idade, cpf)
                VALUES (?, ?, ?)
            """,
                self.txt_nome.get(),
                self.txt_idade.get(),
                self.txt_cpf.get()
            )

            self.conexao.commit()

            messagebox.showinfo(
                "Sucesso",
                "Registro salvo!"
            )

            self.txt_nome.delete(0, tk.END)
            self.txt_idade.delete(0, tk.END)
            self.txt_cpf.delete(0, tk.END)

            self.listar()

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                str(erro)
            )

    def listar(self):

        if not self.conexao:
            return

        try:

            for item in self.tree.get_children():
                self.tree.delete(item)

            cursor = self.conexao.cursor()

            cursor.execute("""
                SELECT Codigo, Nome, idade, cpf
                FROM cad_nome
                ORDER BY Codigo
            """)

            for linha in cursor.fetchall():
                self.tree.insert(
                    "",
                    tk.END,
                    values=(
                        linha.Codigo,
                        linha.Nome,
                        linha.idade,
                        linha.cpf
                    )
                )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                str(erro)
            )


root = tk.Tk()
app = ClienteApp(root)
root.mainloop()