from db_connect import connect_to_db

# upřednostnila jsem AJ, snad nevadí

# funkce pridat_ukol()
# id a i stav ošetřen na straně databáze
def add_task(task_name, task_description, task_status='nezahájeno', conn=None):
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
    print(f"Úkol '{task_name}' byl přidán")

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
        "SELECT id, nazev, popis, stav FROM ukoly WHERE stav = 'nezahájeno' OR stav = 'probíhá'"
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
def update_task(task_id_choice, new_status_choice, conn=None):
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
def delete_task(id_choice, conn=None):
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
    print(f"Úkol ID '{id_choice}' byl smazán")

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