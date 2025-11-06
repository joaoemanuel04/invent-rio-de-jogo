# -*- coding: utf-8 -*-
import sqlite3 as sql

def criar_banco_de_dados():
    """
    Cria as tabelas Usuarios e Jogos (com a relação entre elas)
    se elas ainda não existirem.
    """
    try:
        con = sql.connect('games.db')
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        # Tabela 1: Usuarios (Simplificada - senha é validada na API)
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE
            )
            """
        )

        # Tabela 2: Jogos (com user_id)
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Jogos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                plataforma TEXT,
                lancamento DATE,
                status VARCHAR(20) NOT NULL CHECK (status IN ('Jogando', 'Zerado', 'Nao jogado')),
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Usuarios(id) ON DELETE CASCADE
            )
            """
        )
        
        con.commit()
        print("Banco de dados verificado/criado com sucesso.")

    except sql.Error as e:
        print(f"Erro ao criar o banco de dados: {e}")
    finally:
        if con:
            con.close()

def get_or_create_user_id_local(username):
    """
    Verifica se o usuário existe localmente. Se não, cria.
    Retorna o ID local do usuário.
    """
    try:
        con = sql.connect('games.db')
        cur = con.cursor()
        
        # 1. Tenta buscar o usuário
        cur.execute("SELECT id FROM Usuarios WHERE username = ?", (username,))
        user_data = cur.fetchone()
        
        if user_data:
            # Usuário encontrado, retorna o ID
            return user_data[0]
        else:
            # 2. Usuário não encontrado, cria um novo
            cur.execute("INSERT INTO Usuarios (username) VALUES (?)", (username,))
            con.commit()
            # Retorna o ID do usuário recém-criado
            return cur.lastrowid
            
    except sql.Error as e:
        print(f"Erro ao buscar/criar usuário local: {e}")
        return None
    finally:
        if con:
            con.close()

# --- Executa a criação do banco ao rodar este script ---
if __name__ == "__main__":
    criar_banco_de_dados()