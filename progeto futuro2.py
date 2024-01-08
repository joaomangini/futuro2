import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        self.label_username = tk.Label(root, text="Username:")
        self.label_password = tk.Label(root, text="Password:")

        self.entry_username = tk.Entry(root)
        self.entry_password = tk.Entry(root, show="*")

        self.label_username.grid(row=0, sticky=tk.E)
        self.label_password.grid(row=1, sticky=tk.E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.grid(columnspan=2)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username == "leo" and password == "123":
            self.root.destroy()
            self.open_main_app()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def open_main_app(self):
        root = tk.Tk()
        app_treinamentos = GerenciamentoTreinamentosApp(root)
        root.mainloop()

class GerenciamentoTreinamentosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciamento de Treinamentos")

        self.criar_banco_dados()

        self.notebook = ttk.Notebook(root)
        self.frame_colaboradores = ttk.Frame(self.notebook)
        self.frame_treinamentos = ttk.Frame(self.notebook)
        self.frame_participacoes = ttk.Frame(self.notebook)

        self.notebook.add(self.frame_colaboradores, text="Colaboradores")
        self.notebook.add(self.frame_treinamentos, text="Treinamentos")
        self.notebook.add(self.frame_participacoes, text="Participações")

        self.notebook.pack(expand=1, fill="both")

        self.tree_colaboradores = ttk.Treeview(self.frame_colaboradores, columns=("ID", "Nome", "Área"))
        self.tree_colaboradores.heading("#0", text="", anchor="w")
        self.tree_colaboradores.heading("ID", text="ID", anchor="w")
        self.tree_colaboradores.heading("Nome", text="Nome", anchor="w")
        self.tree_colaboradores.heading("Área", text="Área", anchor="w")

        self.tree_treinamentos = ttk.Treeview(self.frame_treinamentos, columns=("ID", "Nome", "Data"))
        self.tree_treinamentos.heading("#0", text="", anchor="w")
        self.tree_treinamentos.heading("ID", text="ID", anchor="w")
        self.tree_treinamentos.heading("Nome", text="Nome", anchor="w")
        self.tree_treinamentos.heading("Data", text="Data", anchor="w")

        self.tree_participacoes = ttk.Treeview(self.frame_participacoes, columns=("Colaborador", "Treinamento"))
        self.tree_participacoes.heading("#0", text="", anchor="w")
        self.tree_participacoes.heading("Colaborador", text="Colaborador", anchor="w")
        self.tree_participacoes.heading("Treinamento", text="Treinamento", anchor="w")

        self.tree_colaboradores.pack(expand=1, fill="both")
        self.tree_treinamentos.pack(expand=1, fill="both")
        self.tree_participacoes.pack(expand=1, fill="both")

        self.carregar_dados()

        # Adicionando botões para adicionar e remover colaboradores, treinamentos e participações
        self.btn_adicionar_colaborador = tk.Button(self.frame_colaboradores, text="Adicionar Colaborador", command=self.adicionar_colaborador)
        self.btn_adicionar_colaborador.pack(pady=5)

        self.btn_remover_colaborador = tk.Button(self.frame_colaboradores, text="Remover Colaborador", command=self.remover_colaborador)
        self.btn_remover_colaborador.pack(pady=5)

        self.btn_adicionar_treinamento = tk.Button(self.frame_treinamentos, text="Adicionar Treinamento", command=self.adicionar_treinamento)
        self.btn_adicionar_treinamento.pack(pady=5)

        self.btn_remover_treinamento = tk.Button(self.frame_treinamentos, text="Remover Treinamento", command=self.remover_treinamento)
        self.btn_remover_treinamento.pack(pady=5)

        self.btn_realizar_participacao = tk.Button(self.frame_participacoes, text="Realizar Participação", command=self.realizar_participacao)
        self.btn_realizar_participacao.pack(pady=5)

        self.btn_remover_participacao = tk.Button(self.frame_participacoes, text="Remover Participação", command=self.remover_participacao)
        self.btn_remover_participacao.pack(pady=5)

    def criar_banco_dados(self):
        connection = sqlite3.connect("gerenciamento_treinamentos.db")
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Colaboradores (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            area TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Treinamentos (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            data TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Participacoes (
            colaborador_id INTEGER,
            treinamento_id INTEGER,
            PRIMARY KEY (colaborador_id, treinamento_id),
            FOREIGN KEY (colaborador_id) REFERENCES Colaboradores(id),
            FOREIGN KEY (treinamento_id) REFERENCES Treinamentos(id)
        )
        """)

        connection.commit()
        connection.close()

    def carregar_dados(self):
        self.carregar_colaboradores()
        self.carregar_treinamentos()
        self.carregar_participacoes()

    def carregar_colaboradores(self):
        self.tree_colaboradores.delete(*self.tree_colaboradores.get_children())

        connection = sqlite3.connect("gerenciamento_treinamentos.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Colaboradores")
        colaboradores = cursor.fetchall()

        for colaborador in colaboradores:
            self.tree_colaboradores.insert("", "end", values=colaborador)

        connection.close()

    def carregar_treinamentos(self):
        self.tree_treinamentos.delete(*self.tree_treinamentos.get_children())

        connection = sqlite3.connect("gerenciamento_treinamentos.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Treinamentos")
        treinamentos = cursor.fetchall()

        for treinamento in treinamentos:
            self.tree_treinamentos.insert("", "end", values=treinamento)

        connection.close()

    def carregar_participacoes(self):
        self.tree_participacoes.delete(*self.tree_participacoes.get_children())

        connection = sqlite3.connect("gerenciamento_treinamentos.db")
        cursor = connection.cursor()

        cursor.execute("""
        SELECT Colaboradores.nome, Treinamentos.nome
        FROM Participacoes
        JOIN Colaboradores ON Participacoes.colaborador_id = Colaboradores.id
        JOIN Treinamentos ON Participacoes.treinamento_id = Treinamentos.id
        """)

        participacoes = cursor.fetchall()

        for participacao in participacoes:
            self.tree_participacoes.insert("", "end", values=participacao)

        connection.close()

    def adicionar_colaborador(self):
        nome = simpledialog.askstring("Adicionar Colaborador", "Nome do Colaborador:")
        area = simpledialog.askstring("Adicionar Colaborador", "Área do Colaborador:")

        connection = sqlite3.connect("gerenciamento_treinamentos.db")
        cursor = connection.cursor()

        cursor.execute("INSERT INTO Colaboradores (nome, area) VALUES (?, ?)", (nome, area))

        connection.commit()
        connection.close()

        self.carregar_colaboradores()

    def remover_colaborador(self):
        item_selecionado = self.tree_colaboradores.selection()
        if item_selecionado:
            colaborador_id = self.tree_colaboradores.item(item_selecionado, "values")[0]

            connection = sqlite3.connect("gerenciamento_treinamentos.db")
            cursor = connection.cursor()

            cursor.execute("DELETE FROM Colaboradores WHERE id=?", (colaborador_id,))

            connection.commit()
            connection.close()

            self.carregar_colaboradores()
        else:
            messagebox.showwarning("Aviso", "Selecione um colaborador para remover.")

    def adicionar_treinamento(self):
        nome = simpledialog.askstring("Adicionar Treinamento", "Nome do Treinamento:")
        data = simpledialog.askstring("Adicionar Treinamento", "Data do Treinamento (YYYY-MM-DD):")

        connection = sqlite3.connect("gerenciamento_treinamentos.db")
        cursor = connection.cursor()

        cursor.execute("INSERT INTO Treinamentos (nome, data) VALUES (?, ?)", (nome, data))

        connection.commit()
        connection.close()

        self.carregar_treinamentos()

    def remover_treinamento(self):
        item_selecionado = self.tree_treinamentos.selection()
        if item_selecionado:
            treinamento_id = self.tree_treinamentos.item(item_selecionado, "values")[0]

            connection = sqlite3.connect("gerenciamento_treinamentos.db")
            cursor = connection.cursor()

            cursor.execute("DELETE FROM Treinamentos WHERE id=?", (treinamento_id,))

            connection.commit()
            connection.close()

            self.carregar_treinamentos()
        else:
            messagebox.showwarning("Aviso", "Selecione um treinamento para remover.")

    def realizar_participacao(self):
        colaborador_id = simpledialog.askinteger("Realizar Participação", "ID do Colaborador:")
        treinamento_id = simpledialog.askinteger("Realizar Participação", "ID do Treinamento:")

        connection = sqlite3.connect("gerenciamento_treinamentos.db")
        cursor = connection.cursor()

        cursor.execute("INSERT INTO Participacoes (colaborador_id, treinamento_id) VALUES (?, ?)",
                       (colaborador_id, treinamento_id))

        connection.commit()
        connection.close()

        self.carregar_participacoes()

    def remover_participacao(self):
        item_selecionado = self.tree_participacoes.selection()
        if item_selecionado:
            colaborador_id = self.tree_participacoes.item(item_selecionado, "values")[0]
            treinamento_id = self.tree_participacoes.item(item_selecionado, "values")[1]

            connection = sqlite3.connect("gerenciamento_treinamentos.db")
            cursor = connection.cursor()

            cursor.execute("DELETE FROM Participacoes WHERE colaborador_id=? AND treinamento_id=?",
                           (colaborador_id, treinamento_id))

            connection.commit()
            connection.close()

            self.carregar_participacoes()
        else:
            messagebox.showwarning("Aviso", "Selecione uma participação para remover.")

def main():
    root = tk.Tk()
    app_login = LoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
