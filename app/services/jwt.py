from datetime import datetime, timedelta

from app.models.domain.users import User
from app.models.schemas.jwt import JWTMeta, JWTUser
from pydantic import ValidationError

import jwt

ALGORITHM = "HS256"
JWT_SUBJECT = "access"
ACCESS_TOKEN_EXPIRE_MINUTE = 60 * 24 * 7  # Semana


def create_jwt_token(
    *,
    jwt_content: dict[str, str],
    secret_key: str,
    expires_delta: datetime,
) -> str:
    to_enconde = jwt_content.copy()
    expire = datetime.utcnow() + expires_delta

    to_enconde.update(JWTMeta(exp=expire, sub=JWT_SUBJECT).dict())
    return jwt.encode(to_enconde, secret_key, algorithm=ALGORITHM)


def create_access_token_for_user(user: User, secret_key: str) -> str:
    return create_jwt_token(
        jwt_content=JWTUser(email=user.email).dict(),
        secret_key=secret_key,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE),  # type: ignore
    )


def get_email_from_token(token: str, secret_key: str) -> str:
    try:
        return JWTUser(**jwt.decode(token, secret_key, algorithms=[ALGORITHM])).email
    except jwt.PyJWKError as decode_error:
        raise ValueError("unable to decode JWT token") from decode_error
    except ValidationError as validation_error:
        raise ValueError("malformed payload in token") from validation_error
