from datetime import datetime

import mysql.connector
from mysql.connector import Error
from mysql.connector.errors import IntegrityError
import pytest

from config import load_config
from db_connect import connect_to_db

# funkce vytvoreni_tabulky() - upřednostnila jsem AJ, snad nevadí
# Vytvoření tabulky úkoly pokud neexistuje pro testovací databázi
def create_table_if_not_exist(cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ukoly (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev VARCHAR(100) NOT NULL,
                popis VARCHAR(250) NOT NULL,
                stav ENUM('nezahájeno', 'hotovo', 'probíhá') NOT NULL DEFAULT 'nezahájeno',
                datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
""")
    
    except Error as e:
        print(f"Chyba při vytváření tabulky: {e}")

# Fixture pro připojení k testovací databázi
@pytest.fixture(scope="module")
def db():
    conn = connect_to_db(testing=True) #config nemusím předávat, protože v podmínce je, že pokud žádný config nepředám - nastaví se None a fce tedy použije load_config(testing=testing) - a ve fci load_config bude předáno testing=True - takže se načte testovací databáze
    cursor = conn.cursor()
    create_table_if_not_exist(cursor)
    yield cursor
    conn.rollback()
    cursor.close()
    conn.close()

# Fixture pro přípravu na testovnání před každým testem - vyčistí tabulku a vloží úkol
@pytest.fixture(autouse=True)
def seed_test_data(db):
    # Vyčistí tabulku
    db.execute("SET FOREIGN_KEY_CHECKS = 0")
    db.execute("TRUNCATE TABLE tasks")
    db.execute("SET FOREIGN_KEY_CHECKS = 1")

    # vloží úkol
    db.execute("""
        INSERT INTO ukoly (id, nazev, popis, stav)
        VALUES (1, 'Odevzdat projekt 6', 'Jedná se o projektu pro kurz Engeto, který je třeba dokončit a odevzdat již co nejdříve')
    """)
    db.connection.commit()



    

        

