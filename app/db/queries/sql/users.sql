--name: create-new-user<!
INSERT INTO users (
        email,
        salt,
        hashed_password,
        is_active,
        is_superuser
    )
VALUES(
        :email,
        :salt,
        :hashed_password,
        :is_active,
        :is_superuser
    )
RETURNING id,
    is_active,
    is_superuser,
    created_at,
    updated_at;
-- name: update-user-by-email<!
UPDATE users
SET email = :new_email
WHERE email = :email
RETURNING updated_at;
-- name:get-user-by-email^
SELECT id,
    email,
    hashed_password,
    salt,
    created_at,
    updated_at
FROM users
WHERE email = :email
LIMIT 1;