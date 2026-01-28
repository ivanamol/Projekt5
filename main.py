from repository import connect_to_db, create_table_if_not_exists, add_task, show_tasks, update_task, delete_task, get_filtered_tasks, get_all_tasks

# funkce hlavni_menu() - upřednostnila jsem AJ, snad nevadí
def main_menu():
    # vytvářím tabulku v "produkci", pokud tabulka neexisuje, ať je kam úkol uložit - potřebovala jsem ošetřit, pokud zde spojení selže - nemohlo by se předat do cursoru
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
                        print("Zadané ID neexistuje\n")
                        continue

                    new_status_choice = input("\nZadej nový status úkolu (probíhá/hotovo): ").lower().strip()

                    if new_status_choice not in valid_statuses:
                        print("Zadán nevalidní stav, aktualizace neproběhla.\n")
                        continue

                    update_task(task_id_choice, new_status_choice)
                    break

                else:
                    print("\nNejsou žádné úkoly k aktualizaci, seznam je prázdný.")
                    break

        elif user_choice == "4":
            all_task_list = get_all_tasks()
            while True:
                if all_task_list:
                    show_tasks(all_task_list)
                    try:
                        task_id_choice = int(input("Zadejte ID úkolu pro smazání: "))
                    except ValueError:
                        print("Zadáno nevalidní id, smazání neproběhlo.\n")
                        continue

                    all_ids = [task[0] for task in all_task_list]
                    if task_id_choice in all_ids:
                        delete_task(task_id_choice)
                        break
                    else:
                        print("Zadáno nevalidní id, aktualizace neproběhla.\n")
                
                else:
                    print("Nejsou žádné úkoly ke smazání, seznam je prázdný.")
                    break

        elif user_choice == "5":
            print("\nKonec programu.")
            break
        
        else:
            print("Zadali jste neplatnou volbu, volba musí být od 1 do 5.")

if __name__ == "__main__":
    main_menu()