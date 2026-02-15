import pytest

from db_connect import connect_to_db
from repository import add_task, add_task_to_db, create_table_if_not_exists, get_all_tasks, get_filtered_tasks, update_task, delete_task


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
    inputy = iter(["Název test add_task", "Popis úkolu1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputy))
    add_task(conn=db_conn)
    captured = capsys.readouterr()
    tasks = get_all_tasks(conn=db_conn)
    assert any(task[1] == "Název test add_task" for task in tasks)
    assert "Úkol 'Název test add_task' byl přidán." in captured.out


# Negativní test funkce add_task - zadání prázdného jména
def test_add_task_empty_name(db_conn, monkeypatch, capsys):
    inputy = iter(["", "OK název", "OK popis"]) # druhý a třetí input nutný pro ukončení testu
    monkeypatch.setattr("builtins.input", lambda _: next(inputy))
    add_task(conn=db_conn)
    captured = capsys.readouterr()
    tasks = get_all_tasks(conn=db_conn)
    assert all((task[1]) != "" for task in tasks)
    assert "Zadali jste prázdný vstup do názvu úkolu." in captured.out


# Pozitivní test funkce update_task
def test_update_task(db_conn, monkeypatch, capsys):
    add_task_to_db("Název test update_task", "Popis test1", "nezahájeno", conn=db_conn)
    task_id = get_filtered_tasks(conn=db_conn)[0][0]
    inputy = iter([str(task_id), "probíhá"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputy))
    update_task(conn=db_conn)
    captured = capsys.readouterr()
    updated = get_filtered_tasks(conn=db_conn)[0]
    assert updated[-1] == "probíhá"
    assert f"Úkol ID '{task_id}' byl aktualizován, aktuální stav: 'probíhá'" in captured.out


# Negativní test funkce update_task - zadání neplatného id - jiné než číslo
def test_update_task_fail_id(db_conn, monkeypatch, capsys):
    add_task_to_db("Název fail0 update_task", "Popis0 fail id", "nezahájeno", conn=db_conn)
    add_task_to_db("Název fail1 update_task", "Popis1 fail id", "probíhá", conn=db_conn)
    task_id_1 = get_filtered_tasks(conn=db_conn)[1][0]
    inputy = iter(["text, no number", str(task_id_1), "hotovo"]) # druhý a třetí input nutný pro ukončení testu
    monkeypatch.setattr("builtins.input", lambda _: next(inputy))
    update_task(conn=db_conn)
    captured = capsys.readouterr()
    assert "Nezadáno id, aktualizace neproběhla." in captured.out
    updated = get_filtered_tasks(conn=db_conn)[0]
    assert updated[-1] == "nezahájeno" # ověření, že stav zůstává stále stejný jako na začátku


# Pozitivní test funkce delete_task
def test_delete_task(db_conn, monkeypatch, capsys):
    add_task_to_db("Název test delete", "Popis", "nezahájeno", conn=db_conn)
    tasks = get_all_tasks(conn=db_conn)
    task_id = next(task[0] for task in tasks if task[1] == "Název test delete")
    inputy = iter([str(task_id)])
    monkeypatch.setattr("builtins.input", lambda _: next(inputy))
    delete_task(conn=db_conn)
    captured = capsys.readouterr()
    assert f"Úkol ID '{task_id}' byl smazán." in captured.out
    tasks_after = get_all_tasks(conn=db_conn)
    assert all(task[0] != task_id for task in tasks_after)


# Negativní test funkce delete_task - zadání chybného id - nečíselné
def test_delete_task_non_numeric_string(db_conn, monkeypatch, capsys):
    add_task_to_db("Název test", "Popis", "nezahájeno", conn=db_conn)
    tasks = get_all_tasks(conn=db_conn)
    task_id = next(task[0] for task in tasks if task[1] == "Název test") # id pro následné ukončení testu
    inputy = iter(["a", str(task_id)]) # druhý input nutný pro ukončení testu
    monkeypatch.setattr("builtins.input", lambda _: next(inputy))
    delete_task(conn=db_conn)
    captured = capsys.readouterr()
    tasks_after = get_all_tasks(conn=db_conn)
    assert "Zadáno nevalidní id, smazání neproběhlo" in captured.out
    assert len(tasks_after) == len(tasks) - 1 # jeden úkol se druhým inputem vymazal pro ukončení testu


# Negativní test funkce delete_task - zadání neexistujícího id
def test_delete_non_existent_id(db_conn, monkeypatch, capsys):
    add_task_to_db("Název úkolu1", "Popis1", "nezahájeno", conn=db_conn)
    tasks = get_all_tasks(conn=db_conn)
    task_id = next(task[0] for task in tasks if task[1] == "Název úkolu1") # id pro následné ukončení testu
    inputy = iter(["999", str(task_id)]) # druhý input nutný pro ukončení testu
    monkeypatch.setattr("builtins.input", lambda _: next(inputy))
    delete_task(conn=db_conn)
    captured = capsys.readouterr()
    tasks_after = get_all_tasks(conn=db_conn)
    assert "Zadáno nevalidní id, smazání neproběhlo." in captured.out
    assert len(tasks_after) == len(tasks) - 1 # jeden úkol se druhým inputem vymazal pro ukončení testu

