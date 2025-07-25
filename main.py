from email.mime import text
import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk


# Conexão com SQLite
conn = sqlite3.connect("farmacia.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS medicamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    quantidade INTEGER NOT NULL
)
""")
conn.commit()


def cadastrar_medicamento():
    nome = entry_nome.get().strip()
    try:
        qtd = int(entry_qtd.get())
        cursor.execute("INSERT INTO medicamentos (nome, quantidade) VALUES (?, ?)", (nome, qtd))
        conn.commit()
        messagebox.showinfo("Sucesso", "Medicamento cadastrado com sucesso!")
        entry_nome.delete(0, tk.END)
        entry_qtd.delete(0, tk.END)
        listar_medicamentos()
    except ValueError:
        messagebox.showerror("Erro", "Quantidade deve ser um número.")

def listar_medicamentos():
    lista.delete(0, tk.END)
    cursor.execute("SELECT * FROM medicamentos")
    for med in cursor.fetchall():
        lista.insert(tk.END, f"ID: {med[0]} | Nome: {med[1]} | Quantidade: {med[2]}")

def alerta_medicamentos():
    cursor.execute("SELECT nome FROM medicamentos WHERE quantidade <= 0")
    em_falta = cursor.fetchall()
    if em_falta:
        alerta = "\n".join([f"❌ {m[0]}" for m in em_falta])
        messagebox.showwarning("Alerta de falta", alerta)
    else:
        messagebox.showinfo("Estoque", "Todos os medicamentos estão disponíveis.")

def buscar_medicamento():
    nome = simpledialog.askstring("Buscar", "Digite o nome do medicamento:")
    if nome:
        lista.delete(0, tk.END)
        cursor.execute("SELECT * FROM medicamentos WHERE nome LIKE ?", ('%' + nome + '%',))
        resultados = cursor.fetchall()
        if resultados:
            for med in resultados:
                lista.insert(tk.END, f"ID: {med[0]} | Nome: {med[1]} | Quantidade: {med[2]}")
        else:
            messagebox.showinfo("Resultado", "Nenhum medicamento encontrado.")

def editar_medicamento():
    try:
        id_editar = int(simpledialog.askstring("Editar", "Digite o ID do medicamento:"))
        cursor.execute("SELECT * FROM medicamentos WHERE id = ?", (id_editar,))
        med = cursor.fetchone()
        if med:
            novo_nome = simpledialog.askstring("Novo Nome", f"Nome atual: {med[1]}")
            nova_qtd = simpledialog.askinteger("Nova Quantidade", f"Quantidade atual: {med[2]}")
            if novo_nome and nova_qtd is not None:
                cursor.execute("UPDATE medicamentos SET nome = ?, quantidade = ? WHERE id = ?", (novo_nome, nova_qtd, id_editar))
                conn.commit()
                messagebox.showinfo("Sucesso", "Medicamento atualizado!")
                listar_medicamentos()
        else:
            messagebox.showerror("Erro", "ID não encontrado.")
    except:
        messagebox.showerror("Erro", "ID inválido.")

def excluir_medicamento():
    try:
        id_excluir = int(simpledialog.askstring("Excluir", "Digite o ID do medicamento:"))
        cursor.execute("SELECT * FROM medicamentos WHERE id = ?", (id_excluir,))
        med = cursor.fetchone()
        if med:
            confirm = messagebox.askyesno("Confirmação", f"Deseja excluir '{med[1]}'?")
            if confirm:
                cursor.execute("DELETE FROM medicamentos WHERE id = ?", (id_excluir,))
                conn.commit()
                messagebox.showinfo("Sucesso", "Medicamento excluído.")
                listar_medicamentos()
        else:
            messagebox.showerror("Erro", "ID não encontrado.")
    except:
        messagebox.showerror("Erro", "ID inválido.")

janela = tk.Tk()
janela.title("Sistema de Medicamentos")
janela.geometry("800x600")
janela.configure(bg="#e3f2fd")  

fonte_padrao = ("bold", 12)
janela.option_add("*Font", fonte_padrao)

tk.Label(janela, text="Nome do Medicamento").pack(pady=15)
entry_nome = tk.Entry(janela, width=40)
entry_nome.pack(pady=15)


tk.Label(janela, text="Quantidade em Estoque").pack(pady=15)
entry_qtd = tk.Entry(janela, width=40)
entry_qtd.pack(pady=15)
button_width = 25

def show_large_messagebox(title, message):
    top = tk.Toplevel(janela)
    top.title(title)
    top.geometry("500x300")
    top.configure(bg="#f5f6fa")
    tk.Label(top, text=message, bg="#f5f6fa", fg="#222f3e", font=("Segoe UI", 12, "bold"), wraplength=450, justify="left").pack(padx=30, pady=30)
    tk.Button(top, text="OK", command=top.destroy, bg="#54a0ff", fg="#fff", font=("Segoe UI", 10, "bold"), width=10).pack(pady=10)
tk.Button(janela, text="Cadastrar", command=cadastrar_medicamento, bg="#4CAF50", fg="white").pack(pady=15)
tk.Button(janela, text="Listar Medicamentos", command=listar_medicamentos, bg="#0C253F", fg="white").pack(pady=10)
tk.Button(janela, text="Verificar Alerta", command=alerta_medicamentos, bg="#0C253F", fg="white").pack(pady=10)
tk.Button(janela, text="Buscar por Nome", command=buscar_medicamento, bg="#0C253F", fg="white").pack(pady=10)
tk.Button(janela, text="Editar Medicamento", command=editar_medicamento, bg="#0C253F", fg="white").pack(pady=10)
tk.Button(janela, text="Excluir Medicamento", command=excluir_medicamento, bg="#0C253F", fg="white").pack(pady=10)

lista = tk.Listbox(janela, width=100, height=50, bg="#f9fcfd", fg="#333", font=("Arial", 10, "bold"), selectbackground="#dfe6e9", selectforeground="#2d3436")

lista.pack(pady=15)

try:
    img = Image.open("logo.png") 
    img = img.resize((80, 80), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    label_img = tk.Label(janela, image=img_tk, bg="#f5f6fa")
    label_img.pack(pady=5)
except Exception as e:
    pass 
listar_medicamentos() 
janela.mainloop()
conn.close()

def aplicar_tema_claro(widget):
    widget.configure(bg="#f5f6fa")
    for child in widget.winfo_children():
        cls = child.__class__.__name__
        if cls in ["Frame", "LabelFrame"]:
            child.configure(bg="#f5f6fa")
        elif cls == "Label":
            child.configure(bg="#f5f6fa", fg="#222f3e", font=("Segoe UI", 10, "bold"))
        elif cls == "Entry":
            child.configure(bg="#ffffff", fg="#222f3e", insertbackground="#222f3e", relief="groove", font=("Segoe UI", 10))
        elif cls == "Button":
            child.configure(bg="#54a0ff", fg="#fff", activebackground="#2e86de", activeforeground="#fff", relief="flat", font=("Segoe UI", 10, "bold"), cursor="hand2")
        elif cls == "Listbox":
            child.configure(bg="#fff", fg="#222f3e", selectbackground="#c8d6e5", font=("Segoe UI", 10))
        aplicar_tema_claro(child)

aplicar_tema_claro(janela)


def on_resize(event):
    largura = event.width
    if largura < 500:
        lista.configure(width=40)
    elif largura < 700:
        lista.configure(width=60)
    else:
        lista.configure(width=80)

janela.bind("<Configure>", on_resize)
