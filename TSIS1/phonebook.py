import csv
import json
from connect import get_connection

def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            with open("schema.sql", "r", encoding="utf-8") as f:
                cur.execute(f.read())
            with open("procedures.sql", "r", encoding="utf-8") as f:
                cur.execute(f.read())
        conn.commit()

def print_rows(rows):
    if not rows:
        print("No contacts found.")
        return
    for r in rows:
        print(f"ID: {r[0]} | Name: {r[1]} | Email: {r[2]} | Birthday: {r[3]} | Group: {r[4]} | Phones: {r[5]}")

def add_or_update_contact():
    name = input("Name: ").strip()
    email = input("Email: ").strip() or None
    birthday = input("Birthday (YYYY-MM-DD): ").strip() or None
    group = input("Group (Family/Work/Friend/Other): ").strip() or None
    phone = input("Phone: ").strip() or None
    ptype = input("Phone type (home/work/mobile): ").strip() or "mobile"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CALL upsert_contact(%s, %s, %s, %s, %s, %s)",
                (name, email, birthday, group, phone, ptype)
            )
        conn.commit()
    print("Saved.")

def add_phone_to_contact():
    name = input("Contact name: ").strip()
    phone = input("New phone: ").strip()
    ptype = input("Phone type (home/work/mobile): ").strip()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
        conn.commit()
    print("Phone added.")

def move_contact_group():
    name = input("Contact name: ").strip()
    group = input("New group name: ").strip()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL move_to_group(%s, %s)", (name, group))
        conn.commit()
    print("Group updated.")

def search_all():
    q = input("Search query: ").strip()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s)", (q,))
            print_rows(cur.fetchall())

def filter_by_group():
    group = input("Group name: ").strip()
    query = """
        SELECT c.id, c.name, c.email, c.birthday, g.name,
               COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), '')
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE g.name ILIKE %s
        GROUP BY c.id, c.name, c.email, c.birthday, g.name
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (group,))
            print_rows(cur.fetchall())

def search_by_email():
    email_part = input("Email substring: ").strip()
    query = """
        SELECT c.id, c.name, c.email, c.birthday, g.name,
               COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), '')
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE c.email ILIKE %s
        GROUP BY c.id, c.name, c.email, c.birthday, g.name
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (f"%{email_part}%",))
            print_rows(cur.fetchall())

def sort_contacts():
    choice = input("Sort by (1 - name, 2 - birthday, 3 - date added): ").strip()
    order_map = {"1": "c.name ASC", "2": "c.birthday ASC NULLS LAST", "3": "c.created_at DESC"}
    order_clause = order_map.get(choice, "c.name ASC")
    query = f"""
        SELECT c.id, c.name, c.email, c.birthday, g.name,
               COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), '')
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
        ORDER BY {order_clause}
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            print_rows(cur.fetchall())

def paginate_contacts():
    limit = int(input("Page size: ").strip() or "5")
    offset = 0
    while True:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
                rows = cur.fetchall()
        print(f"\n--- Page (offset {offset}) ---")
        print_rows(rows)
        cmd = input("Command (next / prev / quit): ").strip().lower()
        if cmd == "next":
            if len(rows) == limit:
                offset += limit
            else:
                print("End of list.")
        elif cmd == "prev":
            offset = max(0, offset - limit)
        elif cmd == "quit":
            break

def export_json():
    filename = input("JSON filename to export (default contacts.json): ").strip() or "contacts.json"
    query = """
        SELECT c.name, c.email, c.birthday, g.name,
               COALESCE(
                   JSON_AGG(JSON_BUILD_OBJECT('phone', p.phone, 'type', p.type))
                   FILTER (WHERE p.id IS NOT NULL),
                   '[]'
               )
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, c.name, c.email, c.birthday, g.name
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            data = []
            for row in cur.fetchall():
                data.append({
                    "name": row[0],
                    "email": row[1],
                    "birthday": str(row[2]) if row[2] else None,
                    "group": row[3],
                    "phones": row[4] if isinstance(row[4], list) else json.loads(row[4])
                })
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Exported to {filename}.")

def import_json():
    filename = input("JSON filename to import (default contacts.json): ").strip() or "contacts.json"
    with open(filename, "r", encoding="utf-8") as f:
        items = json.load(f)
    with get_connection() as conn:
        with conn.cursor() as cur:
            for item in items:
                name = item.get("name")
                cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
                exists = cur.fetchone()
                if exists:
                    action = input(f"Duplicate '{name}'. Skip or overwrite? (s/o): ").strip().lower()
                    if action == "s":
                        continue
                    cur.execute("DELETE FROM phones WHERE contact_id = %s", (exists[0],))
                email = item.get("email")
                birthday = item.get("birthday")
                group = item.get("group")
                phones = item.get("phones", [])
                if not phones:
                    cur.execute(
                        "CALL upsert_contact(%s, %s, %s, %s, %s, %s)",
                        (name, email, birthday, group, None, None)
                    )
                else:
                    first = phones[0]
                    cur.execute(
                        "CALL upsert_contact(%s, %s, %s, %s, %s, %s)",
                        (name, email, birthday, group, first.get("phone"), first.get("type", "mobile"))
                    )
                    for ph in phones[1:]:
                        cur.execute(
                            "CALL add_phone(%s, %s, %s)",
                            (name, ph.get("phone"), ph.get("type", "mobile"))
                        )
        conn.commit()
    print("JSON import complete.")

def import_csv():
    filename = input("CSV filename to import (default contacts.csv): ").strip() or "contacts.csv"
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        with get_connection() as conn:
            with conn.cursor() as cur:
                for row in reader:
                    cur.execute(
                        "CALL upsert_contact(%s, %s, %s, %s, %s, %s)",
                        (
                            row.get("name"),
                            row.get("email") or None,
                            row.get("birthday") or None,
                            row.get("group") or None,
                            row.get("phone") or None,
                            row.get("type") or "mobile"
                        )
                    )
            conn.commit()
    print("CSV import complete.")

def delete_by_identifier():
    ident = input("Name or phone to delete: ").strip()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL delete_contact(%s)", (ident,))
        conn.commit()
    print("Deleted.")

def main():
    init_db()
    actions = {
        "1": ("Add / Update contact", add_or_update_contact),
        "2": ("Add phone to contact", add_phone_to_contact),
        "3": ("Move contact to group", move_contact_group),
        "4": ("Search contacts (name/email/phone)", search_all),
        "5": ("Filter by group", filter_by_group),
        "6": ("Search by email", search_by_email),
        "7": ("Sort contacts", sort_contacts),
        "8": ("Paginated view", paginate_contacts),
        "9": ("Export to JSON", export_json),
        "10": ("Import from JSON", import_json),
        "11": ("Import from CSV", import_csv),
        "12": ("Delete contact", delete_by_identifier)
    }
    while True:
        print("\n=== PhoneBook TSIS 1 ===")
        for k, v in actions.items():
            print(f"{k}. {v[0]}")
        print("0. Exit")
        choice = input("Select option: ").strip()
        if choice == "0":
            break
        action = actions.get(choice)
        if action:
            try:
                action[1]()
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()