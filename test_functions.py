import pytest

from db_connect import connect_to_db
from repository import create_table_if_not_exists, add_task, get_all_tasks

# Fixture pro připojení k testovací databázi
@pytest.fixture(scope="module") # Chci aby se mi otevřelo připojení a trvalo než se provedou všechny testy, ať se pořád neotevírá a nezavírá, fixture clear_test_data mi vždy data připraví - vyčistí před každám jednotlivým testem, tak by to mělo být ok
def db_conn():
    conn = connect_to_db(testing=True)
    yield conn
    conn.close()

# Fixure pro případné vytvoření tabulky ukoly, pokud neexistuje
@pytest.fixture(scope="module", autouse= True)
def create_table(db_conn):
    cursor = db_conn.cursor()
    create_table_if_not_exists(cursor)
    db_conn.commit()
    cursor.close()

# Fixture pro vyčištění dat před každým jednotlivým testem
@pytest.fixture(autouse=True)
def clear_test_data(db_conn):
    cursor = db_conn.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor.execute("TRUNCATE TABLE ukoly")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    db_conn.commit()
    cursor.close()



# Pozitivní test funkce add_task()
def test_add_task(db_conn, monkeypatch, capsys):
    inputy = iter(["Název úkolu 1 test", "Popis úkolu1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputy))
    add_task(conn=db_conn)
    tasks = get_all_tasks(conn=db_conn)
    assert any(task[1] == "Název úkolu 1 test" for task in tasks)
    captured = capsys.readouterr()
    assert "Úkol 'Název úkolu 1 test' byl přidán." in captured.out


# Negativní test funkce add_task - zadání prázdného jména
def test_add_task_empty_name(db_conn, monkeypatch, capsys):
    inputy = iter(["", "OK název", "OK popis"]) # druhý a třetí input nutný pro ukončení testu
    monkeypatch.setattr("builtins.input", lambda _: next(inputy))
    add_task(conn=db_conn)
    captured = capsys.readouterr()
    assert "Zadali jste prázdný vstup do názvu úkolu." in captured.out




