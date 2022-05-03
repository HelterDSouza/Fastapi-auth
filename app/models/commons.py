import datetime

from pydantic import BaseConfig, BaseModel, Field, validator


class DateTimeModelMixin(BaseModel):
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None

    @validator("updated_at", "created_at", pre=True)
    def default_datetime(cls, value: datetime.datetime) -> datetime.datetime:
        return value or datetime.datetime.now()


class StatusModelMixin(BaseModel):
    is_active: bool = True
    is_superuser: bool = False


class IDModelMixin(BaseModel):
    id_: int = Field(0, alias="id")


class CoreModel(BaseModel):
    class Config(BaseConfig):
        allow_population_by_field_name = True
