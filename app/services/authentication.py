from app.db.erros import UserDoesNotExit
from app.db.repositories.users import UsersRepository
from pydantic import EmailStr


async def check_email_is_taken(user_repo: UsersRepository, email: EmailStr):
    try:
        await user_repo.get_user_by_email(email=email)
    except UserDoesNotExit:
        return False

    return True
