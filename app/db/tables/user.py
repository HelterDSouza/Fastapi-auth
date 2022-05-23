from alembic_utils import pg_trigger
from app.db.base_class import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func


class Users(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    hashed_password = Column(String, index=True, nullable=False)
    salt = Column(Text)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.current_timestamp(),
    )


update_user_modtime = pg_trigger.PGTrigger(
    schema="public",
    signature="update_user_modtime",
    on_entity="public.users",
    definition="""
        BEFORE UPDATE ON public.users
        FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column()
    """,
)


from sqlalchemy import select

a = select(Users.email).where(Users.email == "helterdaniel")
print(a)
