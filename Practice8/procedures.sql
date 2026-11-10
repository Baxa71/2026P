SET search_path TO public;

CREATE OR REPLACE PROCEDURE upsert_contact(n VARCHAR, p VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = n) THEN
        UPDATE contacts SET phone = p WHERE name = n;
    ELSE
        INSERT INTO contacts(name, phone) VALUES(n, p);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    n VARCHAR[],
    p VARCHAR[],
    OUT f_n VARCHAR[],
    OUT f_p VARCHAR[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    f_n := ARRAY[]::VARCHAR[];
    f_p := ARRAY[]::VARCHAR[];

    FOR i IN 1 .. array_length(n, 1) LOOP
        IF p[i] ~ '^[0-9\+\-\(\)\s]{7,15}$' THEN
            CALL upsert_contact(n[i], p[i]);
        ELSE
            f_n := array_append(f_n, n[i]);
            f_p := array_append(f_p, p[i]);
        END IF;
    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact(val VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts WHERE name = val OR phone = val;
END;
$$;