import csv
from connect import get_connection


def create_table(conn):
    sql_query = """
    CREATE TABLE IF NOT EXISTS public.phonebook (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        phone VARCHAR(255) UNIQUE NOT NULL
    );
                """
    with conn.cursor() as cur:
        cur.execute(sql_query)
        conn.commit()
    print("Таблица phonebook успешно создана или уже существует.")


def import_csv(conn, filename="contacts.csv"):
    try:
        with conn.cursor() as cur:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Пропускаем заголовок
                for row in reader:
                    if len(row) == 2:
                        name, phone = row
                        cur.execute("""
                                    INSERT INTO public.phonebook (name, phone)
                                    VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING;
                                    """, (name, phone))
            conn.commit()
        print(f"Данные из {filename} успешно импортированы.")
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
    except Exception as e:
        print(f"Ошибка при импорте: {e}")


def insert_console(conn):
    name = input("Введите имя: ")
    phone = input("Введите телефон: ")
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO public.phonebook (name, phone) VALUES (%s, %s);", (name, phone))
            conn.commit()
            print("Контакт успешно добавлен.")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при добавлении (возможно номер уже есть): {e}")


def update_contact(conn):
    print("Что обновить?")
    print("1. Имя (искать по номеру телефона)")
    print("2. Телефон (искать по имени)")
    choice = input("Выбор (1-2): ")

    with conn.cursor() as cur:
        if choice == '1':
            phone = input("Введите номер телефона: ")
            new_name = input("Введите новое имя: ")
            cur.execute("UPDATE public.phonebook SET name = %s WHERE phone = %s;", (new_name, phone))
        elif choice == '2':
            name = input("Введите имя контакта: ")
            new_phone = input("Введите новый номер: ")
            cur.execute("UPDATE public.phonebook SET phone = %s WHERE name = %s;", (new_phone, name))
        else:
            print("Неверный выбор.")
            return

        if cur.rowcount > 0:
            conn.commit()
            print("Контакт обновлен.")
        else:
            print("Контакт не найден.")


def query_contacts(conn):
    print("Как искать?")
    print("1. Показать всех")
    print("2. Поиск по имени")
    print("3. Поиск по началу номера (префиксу)")
    choice = input("Выбор (1-3): ")

    with conn.cursor() as cur:
        if choice == '1':
            cur.execute("SELECT * FROM public.phonebook ORDER BY id;")
        elif choice == '2':
            name_query = input("Введите имя (или часть): ")
            cur.execute("SELECT * FROM public.phonebook WHERE name ILIKE %s;", (f"%{name_query}%",))
        elif choice == '3':
            prefix = input("Введите префикс (например +7): ")
            cur.execute("SELECT * FROM public.phonebook WHERE phone LIKE %s;", (f"{prefix}%",))
        else:
            print("Неверный выбор.")
            return

        rows = cur.fetchall()
        print("\n--- Результаты ---")
        for row in rows:
            print(f"ID: {row[0]} | Имя: {row[1]} | Телефон: {row[2]}")
        if not rows:
            print("Пусто.")
        print("------------------\n")


def delete_contact(conn):
    name = input("Введите точное имя контакта для удаления: ")
    with conn.cursor() as cur:
        cur.execute("DELETE FROM public.phonebook WHERE name = %s;", (name,))
        if cur.rowcount > 0:
            conn.commit()
            print("Контакт удален.")
        else:
            print("Контакт не найден.")


def main():
    conn = get_connection()
    if not conn:
        return

    create_table(conn)

    while True:
        print("\n=== PHONEBOOK МЕНЮ ===")
        print("1. Импорт из CSV")
        print("2. Добавить вручную")
        print("3. Обновить контакт")
        print("4. Искать контакты")
        print("5. Удалить контакт")
        print("0. Выход")

        choice = input("Действие: ")

        if choice == '1':
            import_csv(conn)
        elif choice == '2':
            insert_console(conn)
        elif choice == '3':
            update_contact(conn)
        elif choice == '4':
            query_contacts(conn)
        elif choice == '5':
            delete_contact(conn)
        elif choice == '0':
            break

    conn.close()
    print("Программа завершена.")


if __name__ == '__main__':
    main()