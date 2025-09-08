import sqlite3 as sql
from enum import Enum

class Status(Enum):
    jogando = "Jogando"
    zerado = "Zerado"
    nao_jogado = "Não jogado"

con = sql.connect('games.db')

with con:
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE Jogos(id INTEGER PRIMARY KEY AUTOINCREMENT ," \
        "nome TEXT, plataforma TEXT, " \
        "lancamento DATE, " \
        "status VARCHAR(20) NOT NULL CHECK (status IN ('Jogando', 'Zerado', 'Nao jogado')))"
    )

