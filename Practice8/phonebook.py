from connect import get_connection

def setup_table():
    conn = get_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    phone VARCHAR(20) NOT NULL
                );
            """)
            conn.commit()
        conn.close()


def search_contacts(pattern):
    conn = get_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_by_pattern(%s);", (pattern,))
            for row in cur.fetchall():
                print(row)
        conn.close()


def upsert_user(name, phone):
    conn = get_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("CALL upsert_contact(%s, %s);", (name, phone))
            conn.commit()
            print(f"Upsert: {name}")
        conn.close()


def bulk_insert(names, phones):
    conn = get_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("CALL bulk_insert_contacts(%s, %s, NULL, NULL);", (names, phones))
            conn.commit()
            f_names, f_phones = cur.fetchone()

            if f_names:
                print("Failed:")
                for n, p in zip(f_names, f_phones):
                    print(f"{n} - {p}")
            else:
                print("Bulk OK")
        conn.close()


def get_paginated(limit, offset):
    conn = get_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
            for row in cur.fetchall():
                print(row)
        conn.close()


def delete_user(val):
    conn = get_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("CALL delete_contact(%s);", (val,))
            conn.commit()
            print(f"Del: {val}")
        conn.close()


if __name__ == "__main__":
    setup_table()

    upsert_user("Alice", "1234567890")
    upsert_user("Alice", "0987654321")

    names = ["Bob", "Char", "Err"]
    phones = ["111222333", "+1-800-55", "bad!"]
    bulk_insert(names, phones)

    search_contacts("Alice")

    get_paginated(2, 0)

    delete_user("Bob")