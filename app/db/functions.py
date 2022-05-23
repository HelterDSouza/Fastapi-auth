from alembic_utils.pg_function import PGFunction

update_updated_at_column = PGFunction(
    schema="public",
    signature="update_updated_at_column()",
    definition="""
    RETURNS TRIGGER AS
    $$
    BEGIN
        NEW.updated_at = now();
        RETURN NEW;
    END;
    $$ language 'plpgsql'
    """,
)
