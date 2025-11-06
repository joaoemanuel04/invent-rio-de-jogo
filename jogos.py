# -*- coding: utf-8 -*-
import sqlite3 as sql

def adicionar(nome, plataforma, lancamento, status, user_id):
    con = sql.connect('games.db')
    bd = con.cursor()
    # Adicionamos user_id ao INSERT
    bd.execute("INSERT INTO Jogos (nome, plataforma, lancamento, status, user_id) VALUES (?, ?, ?, ?, ?)", 
               (nome, plataforma, lancamento, status, user_id))
    con.commit()
    con.close()

def remover(id, user_id):
    con = sql.connect('games.db')
    bd = con.cursor()
    # Garantimos que o usuário só possa deletar o que é dele
    bd.execute("DELETE FROM Jogos WHERE id = ? AND user_id = ?", (id, user_id))
    con.commit()
    con.close()

def editar(id, categoria, valor, user_id):
    """
    Atualiza um único campo (categoria) de um jogo específico com um novo valor.
    """
    try:
        con = sql.connect('games.db')
        bd = con.cursor()
        
        # O uso de if/elif é uma forma segura de determinar a coluna
        # Adicionamos user_id ao UPDATE para segurança
        if categoria == "nome":
            bd.execute("UPDATE Jogos SET nome = ? WHERE id = ? AND user_id = ?", (valor, id, user_id))
        elif categoria == "plataforma":
            bd.execute("UPDATE Jogos SET plataforma = ? WHERE id = ? AND user_id = ?", (valor, id, user_id))
        elif categoria == "status":
            bd.execute("UPDATE Jogos SET status = ? WHERE id = ? AND user_id = ?", (valor, id, user_id))
        else:
            print(f"A categoria '{categoria}' não é válida para edição.")
            return

        con.commit()
        print(f"Jogo ID {id} (Usuário {user_id}) atualizado com sucesso no campo '{categoria}'.")

    except sql.Error as e:
        print(f"Ocorreu um erro ao editar o jogo: {e}")

    finally:
        if con:
            con.close()

def buscar(nome, user_id):
    con = sql.connect('games.db')
    bd = con.cursor()
    # Adicionamos user_id ao SELECT
    bd.execute("SELECT * FROM Jogos WHERE nome LIKE ? AND user_id = ?", ('%'+nome+'%', user_id))
    resultado = bd.fetchall()
    con.close()
    return resultado

def listar(user_id):
    con = sql.connect('games.db')
    bd = con.cursor()
    # Adicionamos user_id ao SELECT
    bd.execute("SELECT * FROM Jogos WHERE user_id = ?", (user_id,))
    resultado = bd.fetchall()
    con.close()
    return resultado