import mysql.connector
from mysql.connector import Error

from config import load_config

# funkce pripojeni_db() - upřednostnila jsem AJ, snad nevadí
def connect_to_db(config=None, testing=False):
    if config is None:
        config = load_config(testing=testing)

    if testing and "test" not in config["database"].lower():
        raise RuntimeError("Varování: Při testování musíš použít testovací DB.")
        
    try:
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
                print(f"Připojení k databázi '{config['database']}' bylo úspěšné.")
                return conn
    except Error as e:
            print(f"Chyba připojení: {e}")
            return None