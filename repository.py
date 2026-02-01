from mysql.connector import Error

from db_connect import connect_to_db

# upřednostnila jsem AJ, snad nevadí

# funkce vytvoreni_tabulky() - pokud ještě daná tabulka neexistuje, ošetřeno, že nelze zadat prázdný vstup u názvu a popisu
def create_table_if_not_exists(cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ukoly (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev VARCHAR(100) NOT NULL,
                popis VARCHAR(250) NOT NULL,
                stav ENUM('nezahájeno', 'hotovo', 'probíhá') NOT NULL DEFAULT 'nezahájeno',
                datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT check_nazev_not_empty CHECK (TRIM(nazev) <> ''),
                CONSTRAINT check_popis_not_empty CHECK (TRIM(popis) <> '')
            )
""")
    
    except Error as e:
        print(f"Chyba při vytváření tabulky: {e}")


# funkce pridat_ukol()
def add_task(conn=None):
    while True:
        task_name = input("Zadejte název úkolu: ").strip()
        if not task_name:
            print("\nZadali jste prázdný vstup do názvu úkolu.")
            continue
        if len(task_name) > 100:
            print("\nZadali jste příliš dlouhý název úkolu, maximální počet znaků je 100.")
            continue
        task_description = input("Zadejte popis úkolu: ").strip()
        if not task_description:
            print("\nZadali jste prázdný vstup do popisu úkolu.")
            continue
        if len(task_description) > 250:
            print("\nZadali jste příliš dlouhý popis úkolu, maximální počet znaků je 250.")
            continue
        add_task_to_db(task_name, task_description, conn=conn)
        break


def add_task_to_db(task_name, task_description, task_status='nezahájeno', conn=None):
    """
    Adds a new task to the database.
    If a connection (conn) is not provided, the function creates its own.
    """
    close_conn = False
    if conn is None:
        conn = connect_to_db()
        close_conn = True
    
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ukoly (nazev, popis, stav) VALUES (%s, %s, %s)", (task_name, task_description, task_status)
    )
    conn.commit()
    print(f"Úkol '{task_name}' byl přidán.")

    cursor.close()
    if close_conn:
        conn.close()
        

def get_filtered_tasks(conn=None):
    """
    Retrieves all tasks from the 'ukoly' table with the status 'probíhá' or 'nezahájeno'.
    If no connection (conn) is provided, the function creates its own.
    """
    close_conn = False
    if conn is None:
        conn = connect_to_db()
        close_conn = True
    
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nazev, popis, stav FROM ukoly WHERE stav = 'nezahájeno' OR stav = 'probíhá' ORDER BY id ASC"
    )
    task_list = cursor.fetchall()

    cursor.close()
    if close_conn:
        conn.close()

    return task_list


# funkce zobrazit_ukoly()
def show_tasks(task_list):
    """
    Displays the task list. If the list is empty, a notification is prompted.
    """
    if task_list:
        print(f"Seznam úkolů:\n")
        for task in task_list:
            print(f"ID: {task[0]}, nazev: {task[1]}, popis: {task[2]}, stav: {task[3]}")
    else:
        print("Seznam je prázdný")
        return None

# funkce aktualizovat_ukol()
def update_task(conn=None):
    filtered_task_list = get_filtered_tasks()
    valid_statuses = ["probíhá", "hotovo"]
    while True:

        if filtered_task_list:
            show_tasks(filtered_task_list)
            try:
                task_id_choice = int(input("\nZadej ID úkolu pro aktualizaci jeho stavu: "))
            except ValueError:
                print("Nezadáno id, aktualizace neproběhla.\n")
                continue
                    
            filtered_ids = [task[0] for task in filtered_task_list]
            if task_id_choice not in filtered_ids:
                print("Zadané ID neexistuje.\n")
                continue

            new_status_choice = input("\nZadej nový status úkolu (probíhá/hotovo): ").lower().strip()

            if new_status_choice not in valid_statuses:
                print("Zadán nevalidní stav, aktualizace neproběhla.\n")
                continue

            update_task_in_db(task_id_choice, new_status_choice, conn=conn)
            break

        else:
            print("\nNejsou žádné úkoly k aktualizaci, seznam je prázdný.")
            break


def update_task_in_db(task_id_choice, new_status_choice, conn=None):
    """
    Updates the status (probíhá/hotovo) of a task in the 'ukoly' table.
    If no connection (conn) is provided, the function creates its own.
    """
    close_conn = False
    if conn is None:
        conn = connect_to_db()
        close_conn = True

    cursor = conn.cursor()
    cursor.execute(
        "UPDATE ukoly SET stav = %s WHERE id = %s", (new_status_choice, task_id_choice)
    )
   
    conn.commit()
    print(f"Úkol ID '{task_id_choice}' byl aktualizován, aktuální stav: '{new_status_choice}'.")

    cursor.close()
    if close_conn:
        conn.close()


# funkce odstranit_ukol()
def delete_task(conn=None):
    all_task_list = get_all_tasks(conn=conn)
    while True:
        if all_task_list:
            show_tasks(all_task_list)
            try:
                task_id_choice = int(input("\nZadejte ID úkolu pro smazání: "))
            except ValueError:
                print("Zadáno nevalidní id, smazání neproběhlo.\n")
                continue

            all_ids = [task[0] for task in all_task_list]
            if task_id_choice in all_ids:
                delete_task_from_db(task_id_choice, conn=conn)
                break
            else:
                print("Zadáno nevalidní id, smazání neproběhlo.\n")
        else:
            print("Nejsou žádné úkoly ke smazání, seznam je prázdný.")
            break


def delete_task_from_db(id_choice, conn=None):
    """
    Deletes a task from the database by its ID.
    If no connection (conn) is provided, the function creates its own.
    """
    close_conn = False
    if conn is None:
        conn = connect_to_db()
        close_conn = True

    cursor = conn.cursor()
    cursor.execute("DELETE FROM ukoly WHERE id = %s", (id_choice,))

    conn.commit()
    print(f"Úkol ID '{id_choice}' byl smazán.")

    cursor.close()
    if close_conn:
        conn.close()


def get_all_tasks(conn=None):
    """
    Returns a list of all tasks from the 'ukoly' table.
    If no connection (conn) is provided, the function creates its own.
    """

    close_conn = False
    if conn is None:
        conn = connect_to_db()
        close_conn = True
    
    cursor = conn.cursor()
    cursor.execute("SELECT id, nazev, popis, stav FROM ukoly")
    result = cursor.fetchall()

    cursor.close()
    if close_conn:
        conn.close()

    return result