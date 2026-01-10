from repository import (add_task, show_tasks, update_task, delete_task, get_filtered_tasks, get_all_tasks)

# funkce hlavni_menu() - upřednostnila jsem AJ, snad nevadí
def main_menu():
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
                    print("\nZadali jste prázdný vstup do popisu úkolu")
                    continue
                if len(task_description) > 250:
                    print("\nZadali jste příliš dlouhý popis úkolu, maximální počet znaků je 250.")
                    continue
                add_task(task_name, task_description)
                break
  

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