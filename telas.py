# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import jogos as jg
from tkinter import ttk, messagebox

# user_id foi adicionado como parâmetro
def janela_buscar(master, tabela, user_id):
    popup = tk.Toplevel(master)
    popup.title("Buscar Jogo")
    popup.geometry("300x150")
    popup.configure(bg="#f2e5b8")

    tk.Label(popup, text="Nome do Jogo:", bg="#f2e5b8").pack(pady=10)
    nome_var = tk.StringVar()
    entry_nome = tk.Entry(popup, textvariable=nome_var, width=30)
    entry_nome.pack(pady=5)

    def buscar():
        nome = nome_var.get()
        for item in tabela.get_children():
            tabela.delete(item)
        # Passa o user_id para a busca
        jogos = jg.buscar(nome, user_id) 
        for jogo in jogos:
            tabela.insert("", "end", values=jogo)
        popup.destroy()

    botao_buscar = tk.Button(popup, text="Buscar", command=buscar, bg="#4a90e2", fg="white", width=10)
    botao_buscar.pack(pady=10)

# user_id foi adicionado como parâmetro
def janela_editar(master, tabela, user_id):
    selected_item = tabela.focus()
    if not selected_item:
        messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione um jogo para editar.")
        return

    jogo_atual = tabela.item(selected_item)['values']
    id_jogo = jogo_atual[0]
    
    valores_originais = {
        "nome": jogo_atual[1],
        "plataforma": jogo_atual[2],
        "status": jogo_atual[4] 
    }

    popup = tk.Toplevel(master)
    popup.title("Edição Rápida")
    popup.geometry("350x200")
    popup.configure(bg="#f2e5b8")
    popup.transient(master)
    popup.grab_set()

    frame = tk.Frame(popup, bg="#f2e5b8", padx=10, pady=10)
    frame.pack(expand=True, fill="both")

    tk.Label(frame, text="Campo para Editar:", bg="#f2e5b8").pack(pady=(0, 5))

    categoria_var = tk.StringVar()
    valor_var = tk.StringVar()

    categorias = list(valores_originais.keys())
    combo_categoria = ttk.Combobox(frame, textvariable=categoria_var, values=categorias, state="readonly", width=30)
    combo_categoria.pack()

    status_options = ["Jogando", "Zerado", "Nao Jogado"]

    tk.Label(frame, text="Novo Valor:", bg="#f2e5b8").pack(pady=(10, 5))

    frame_dinamico = tk.Frame(frame, bg="#f2e5b8")
    frame_dinamico.pack(pady=5)

    def atualizar_widget_de_entrada(event=None):
        for widget in frame_dinamico.winfo_children():
            widget.destroy()

        categoria_selecionada = categoria_var.get()
        status_options = ["Jogando", "Zerado", "Nao Jogado"]

        if categoria_selecionada == "status":
            combo_status = ttk.Combobox(frame_dinamico, textvariable=valor_var, values=status_options, state="readonly", width=30)
            combo_status.pack()
        else:
            entry_valor = tk.Entry(frame_dinamico, textvariable=valor_var, width=33)
            entry_valor.pack()
        
        valor_var.set(valores_originais.get(categoria_selecionada, ""))

    combo_categoria.bind("<<ComboboxSelected>>", atualizar_widget_de_entrada)
    
    combo_categoria.set(categorias[0])
    atualizar_widget_de_entrada()

    def salvar_alteracao():
        categoria_selecionada = categoria_var.get()
        novo_valor = valor_var.get()

        if not categoria_selecionada:
            messagebox.showwarning("Atenção", "Por favor, selecione uma categoria para editar.")
            return
        
        # Passa o user_id para a edição
        jg.editar(id_jogo, categoria_selecionada, novo_valor, user_id)

        for item in tabela.get_children():
            tabela.delete(item)
        # Passa o user_id para listar
        for jogo in jg.listar(user_id):
            tabela.insert("", "end", values=jogo)
        
        messagebox.showinfo("Sucesso", f"O campo '{categoria_selecionada}' foi atualizado!")
        popup.destroy()

    botao_salvar = tk.Button(frame, text="Salvar Alteração", command=salvar_alteracao, bg="#4a90e2", fg="white")
    botao_salvar.pack(pady=15)

# user_id foi adicionado como parâmetro
def janela_excluir(master, tabela, user_id):
    selected_item = tabela.focus()
    if not selected_item:
        messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione um jogo para excluir.")
        return

    jogo_selecionado = tabela.item(selected_item)['values']
    id_jogo = int(jogo_selecionado[0])
    nome_jogo = jogo_selecionado[1]

    resposta = messagebox.askyesno("Confirmação de Exclusão", f"Tem certeza que deseja excluir o jogo '{nome_jogo}'?")
    if resposta:
        # Passa o user_id para remover
        jg.remover(id_jogo, user_id)
        tabela.delete(selected_item)
        messagebox.showinfo("Exclusão Bem-Sucedida", f"O jogo '{nome_jogo}' foi excluído com sucesso.")