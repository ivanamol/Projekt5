from datetime import date, time

import pytest

from config import load_config
from db_connect import connect_to_db
from repository import get_all_tasks

# Fixture pro připojení k testovací databázi
@pytest.fixture(scope="module") # Chci aby se mi otevřelo připojení a trvalo než se provedou všechny testy, ať se pořád neotevírá a nezavírá, fixture clear_test_data mi vždy data připraví - vyčistí před každám jednotlivým testem, tak by to mělo být ok
def db_conn():
    conn = connect_to_db(testing=True)
    yield conn
    conn.close()

# Fixture pro vyčištění dat před každým jednotlivým testem
@pytest.fixture(autouse=True)
def clear_test_data(db_conn):
    cursor = db_conn.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor.execute("TRUNCATE TABLE ukoly")
    cursor.execute("SET FOREIGN_KEY_CHECK = 1")
    db_conn.commit()
    cursor.close()


