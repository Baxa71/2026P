CREATE OR REPLACE PROCEDURE upsert_contact(
    p_name VARCHAR,
    p_email VARCHAR,
    p_birthday DATE,
    p_group_name VARCHAR,
    p_phone VARCHAR,
    p_phone_type VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_group_id INT;
    v_contact_id INT;
BEGIN
    IF p_group_name IS NOT NULL AND p_group_name <> '' THEN
        INSERT INTO groups (name) VALUES (p_group_name)
        ON CONFLICT (name) DO NOTHING;
        SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    END IF;

    INSERT INTO contacts (name, email, birthday, group_id)
    VALUES (p_name, p_email, p_birthday, v_group_id)
    ON CONFLICT (name) DO UPDATE
    SET email = EXCLUDED.email,
        birthday = EXCLUDED.birthday,
        group_id = EXCLUDED.group_id
    RETURNING id INTO v_contact_id;

    IF p_phone IS NOT NULL AND p_phone <> '' THEN
        INSERT INTO phones (contact_id, phone, type)
        VALUES (v_contact_id, p_phone, p_phone_type)
        ON CONFLICT (contact_id, phone) DO UPDATE
        SET type = EXCLUDED.type;
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INT;
BEGIN
    SELECT id INTO v_contact_id FROM contacts WHERE name = p_contact_name;
    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type)
    ON CONFLICT (contact_id, phone) DO UPDATE
    SET type = EXCLUDED.type;
END;
$$;

CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_group_id INT;
BEGIN
    INSERT INTO groups (name) VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;

    UPDATE contacts SET group_id = v_group_id WHERE name = p_contact_name;
END;
$$;

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    contact_id INT,
    name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phones TEXT
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.name,
        c.email,
        c.birthday,
        g.name,
        COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), '')
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    GROUP BY c.id, c.name, c.email, c.birthday, g.name
    HAVING c.name ILIKE '%' || p_query || '%'
        OR c.email ILIKE '%' || p_query || '%'
        OR BOOL_OR(p.phone ILIKE '%' || p_query || '%');
END;
$$;

CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(
    contact_id INT,
    name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phones TEXT,
    created_at TIMESTAMP
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.name,
        c.email,
        c.birthday,
        g.name,
        COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), ''),
        c.created_at
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
    ORDER BY c.id
    LIMIT p_limit OFFSET p_offset;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact(p_identifier VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts
    WHERE name = p_identifier
       OR id IN (SELECT contact_id FROM phones WHERE phone = p_identifier);
END;
$$;