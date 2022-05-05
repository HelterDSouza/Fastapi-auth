from app.models.commons import (
    CoreModel,
    DateTimeModelMixin,
    IDModelMixin,
    StatusModelMixin,
)
from app.services import hash_password
from pydantic import EmailStr


class User(CoreModel):
    email: EmailStr


class UserInDB(IDModelMixin, DateTimeModelMixin, User, StatusModelMixin):
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str) -> bool:
        return hash_password.verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str) -> None:

        self.salt = hash_password.generate_salt()
        self.hashed_password = hash_password.get_password_hash(self.salt + password)
