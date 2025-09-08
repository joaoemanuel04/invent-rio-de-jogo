# -*- coding: utf-8 -*-
import sqlite3 as sql
def adicionar(nome, plataforma, lancamento, status):
    con = sql.connect('games.db')
    bd = con.cursor()
    bd.execute("INSERT INTO Jogos (nome, plataforma, lancamento, status) VALUES (?, ?, ?, ?)", (nome, plataforma, lancamento, status))
    con.commit()
    con.close()

def remover(id):
    con = sql.connect('games.db')
    bd = con.cursor()
    bd.execute("DELETE FROM Jogos WHERE id = ?", (id, ))
    con.commit()
    con.close()

def editar(id, categoria, valor):
    """
    Atualiza um único campo (categoria) de um jogo específico com um novo valor.
    """
    try:
        con = sql.connect('games.db')
        bd = con.cursor()
        
        # O uso de if/elif é uma forma segura de determinar a coluna
        if categoria == "nome":
            bd.execute("UPDATE Jogos SET nome = ? WHERE id = ?", (valor, id))
        elif categoria == "plataforma":
            bd.execute("UPDATE Jogos SET plataforma = ? WHERE id = ?", (valor, id))
        elif categoria == "status":
            bd.execute("UPDATE Jogos SET status = ? WHERE id = ?", (valor, id))
        else:
            # Informa caso a categoria seja inválida para evitar erros silenciosos
            print(f"A categoria '{categoria}' não é válida para edição.")
            return

        con.commit()
        print(f"Jogo ID {id} atualizado com sucesso no campo '{categoria}'.")

    except sql.Error as e:
        print(f"Ocorreu um erro ao editar o jogo: {e}")

    finally:
        if con:
            con.close()

def buscar(nome):
    con = sql.connect('games.db')
    bd = con.cursor()
    bd.execute("SELECT * FROM Jogos WHERE nome LIKE ?", ('%'+nome+'%',))
    resultado = bd.fetchall()
    con.close()
    return resultado

def listar():
    con = sql.connect('games.db')
    bd = con.cursor()
    bd.execute("SELECT * FROM Jogos")
    resultado = bd.fetchall()
    con.close()
    return resultado