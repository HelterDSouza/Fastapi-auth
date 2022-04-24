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
    updated_at