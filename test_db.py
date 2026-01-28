from mysql.connector.errors import IntegrityError, DatabaseError
import pytest

from db_connect import connect_to_db
from repository import create_table_if_not_exists

# Fixture pro připojení k testovací databázi
@pytest.fixture(scope="module")
def db():
    conn = connect_to_db(testing=True)
    cursor = conn.cursor()
    create_table_if_not_exists(cursor)
    yield cursor
    conn.rollback()
    cursor.close()
    conn.close()

# Fixture pro přípravu na testovnání před každým testem - vyčistí tabulku a vloží úkol
@pytest.fixture(autouse=True)
def seed_test_data(db):
    # Vyčistí tabulku
    db.execute("SET FOREIGN_KEY_CHECKS = 0")
    db.execute("TRUNCATE TABLE ukoly")
    db.execute("SET FOREIGN_KEY_CHECKS = 1")

    # vloží úkol
    db.execute("""
        INSERT INTO ukoly (id, nazev, popis, stav)
        VALUES (1, 'Odevzdat projekt 6', 'Jedná se o projektu pro kurz Engeto, který je třeba dokončit a odevzdat již co nejdříve', 'nezahájeno')
    """)

# Pozitivní test - v databázi se nenachází úkol bez názvu - s prázdným řetězcem
def test_nazev_not_empty(db):
    db.execute("SELECT nazev FROM ukoly WHERE TRIM(nazev) = ''")
    assert db.fetchall() == []

# Pozitivní test - v databázi se nenachází test s hodnotou NULL
def test_nazev_not_null(db):
    db.execute("SELECT nazev FROM ukoly WHERE nazev IS NULL")
    assert db.fetchall() == []

# Negativní test - vložení úkolu s prázdným řetězcem jako názvem
def test_insert_nazev_empty(db):
    with pytest.raises((IntegrityError, DatabaseError), match="violated"):
        db.execute("INSERT INTO ukoly (nazev, popis, stav) VALUES (%s, %s, %s)", ("", "popis", "nezahájeno"))

# Negativní test - vložení úkolu bez názvu (absence hodnoty)
def test_insert_nazev_null(db):
    with pytest.raises(IntegrityError):
        db.execute("INSERT INTO ukoly (nazev, popis, stav) VALUES (%s, %s, %s)", (None, "popis", "nezahájeno"))

# Pozitivní test přidání nového úkolu bez statusu - nastaví se status nezahájeno
def test_stav_default_nezahajeno(db):
    db.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)",("Nazev_test1", "Popis_test1"))
    db.execute("SELECT stav FROM ukoly ORDER BY id DESC LIMIT 1")
    (stav,) = db.fetchone()
    assert stav == 'nezahájeno'

# Negativní test přidání úkolu s nevalidním statusem
def test_insert_invalid_stav(db):
    with pytest.raises(DatabaseError):
        db.execute("INSERT INTO ukoly (nazev, popis, stav) VALUES (%s, %s, %s)", ("Název", "Popis", "nevalidní_stav"))

    

        

