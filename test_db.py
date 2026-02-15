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
        VALUES (1, 'Odevzdat projekt 5', 'Jedná se o projektu pro kurz Engeto, který je třeba dokončit a odevzdat již co nejdříve', 'nezahájeno')
    """)


# Test - vložení úkolu do databáze
def test_insert_task(db):
    db.execute("INSERT INTO ukoly (nazev, popis, stav) VALUES (%s, %s, %s)", ('Test název', 'popis', 'nezahájeno'))
    db.execute("SELECT nazev FROM ukoly WHERE nazev = %s", ('Test název',))
    result = db.fetchone()
    assert result[0] == 'Test název'


# Test - vložení úkolu s prázdným řetězcem jako názvem
def test_insert_nazev_empty(db):
    with pytest.raises((IntegrityError, DatabaseError), match="violated"):
        db.execute("INSERT INTO ukoly (nazev, popis, stav) VALUES (%s, %s, %s)", ('', 'popis', 'nezahájeno'))


# Test - vložení úkolu bez názvu (absence hodnoty)
def test_insert_nazev_null(db):
    with pytest.raises(IntegrityError):
        db.execute("INSERT INTO ukoly (nazev, popis, stav) VALUES (%s, %s, %s)", (None, 'popis', 'nezahájeno'))


# Test přidání nového úkolu bez statusu - nastaví se status nezahájeno
def test_stav_default_nezahajeno(db):
    db.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", ('Nazev_test1', 'Popis_test1'))
    db.execute("SELECT stav FROM ukoly ORDER BY id DESC LIMIT 1")
    (stav,) = db.fetchone()
    assert stav == 'nezahájeno'


# Test přidání úkolu s nevalidním statusem
def test_insert_invalid_stav(db):
    with pytest.raises(DatabaseError):
        db.execute("INSERT INTO ukoly (nazev, popis, stav) VALUES (%s, %s, %s)", ('Název', 'Popis', 'nevalidní_stav'))


# Test aktualizace úkolu
def test_update_task(db):
    db.execute("INSERT INTO ukoly (nazev, popis, stav) VALUES (%s, %s, %s)", ('Test název 2', 'popis', 'nezahájeno'))
    db.execute("UPDATE ukoly SET stav = %s WHERE nazev = %s", ('hotovo', 'Test název 2'))
    db.execute("SELECT stav FROM ukoly WHERE nazev = %s", ('Test název 2',))
    result = db.fetchone()
    assert result[0] == 'hotovo'


# Test aktualizace úkolu - zadán nesprávný status
def test_update_invalid_stav(db):
    with pytest.raises(DatabaseError):
        db.execute("UPDATE ukoly SET stav = %s WHERE id = %s", ('nevalidní', 1))


# Test smazání úkolu
def test_delete_task(db):
    db.execute("INSERT INTO ukoly (nazev, popis, stav) VALUES (%s, %s, %s)", ('Test název delete', 'popis', 'nezahájeno'))
    db.execute("DELETE FROM ukoly WHERE nazev = %s", ('Test název delete',))
    db.execute("SELECT * FROM ukoly WHERE nazev = %s", ('Test název delete',))
    result = db.fetchone()
    assert result is None


# Test mazání neexistujícího úkolu
def test_delete_invalid(db):
    db.execute("DELETE FROM ukoly WHERE id = %s", (999,))
    assert db.rowcount == 0


        

