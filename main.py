from repository import (
    connect_to_db,
    create_table_if_not_exists,
    add_task,
    show_tasks,
    update_task,
    delete_task,
    get_filtered_tasks,
)


# funkce hlavni_menu() - upřednostnila jsem AJ, snad nevadí
def main_menu():
    # vytvářím tabulku v "produkci", pokud tabulka neexisuje, ať je kam úkol
    # uložit - potřebovala jsem ošetřit, pokud zde spojení selže - nemohlo by
    # se předat do cursoru
    conn = connect_to_db()
    if not conn:
        return
    cursor = conn.cursor()
    create_table_if_not_exists(cursor)
    conn.commit()
    cursor.close()
    conn.close()

    while True:
        print(
            "\nSprávce úkolů - Hlavní menu\n"
            "1. Přidat úkol\n"
            "2. Zobrazit úkoly\n"
            "3. Aktualizovat úkoly\n"
            "4. Odstranit úkol\n"
            "5. Konec programu\n"
        )

        user_choice = input("Vyberte možnost (1-5): ")

        if user_choice == "1":
            add_task()

        elif user_choice == "2":
            filtered_task_list = get_filtered_tasks()
            show_tasks(filtered_task_list)

        elif user_choice == "3":
            update_task()

        elif user_choice == "4":
            delete_task()

        elif user_choice == "5":
            print("\nKonec programu.")
            break

        else:
            print("Zadali jste neplatnou volbu, volba musí být od 1 do 5.")


if __name__ == "__main__":
    main_menu()
