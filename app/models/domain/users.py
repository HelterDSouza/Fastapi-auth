from app.models.commons import CoreModel, DateTimeModelMixin, IDModelMixin
from app.utils.security import HashPassword
from pydantic import BaseModel, EmailStr


class User(CoreModel):
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False


class UserInDB(IDModelMixin, DateTimeModelMixin, User):
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str) -> bool:
        return HashPassword.verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str) -> None:

        self.salt = HashPassword.generate_salt()
        self.hashed_password = HashPassword.get_password_hash(self.salt + password)
