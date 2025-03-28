from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    ValidationError,
    constr,
    StringConstraints
    )
from api.utils.email import Email # TODO: Check better way to use this class with pydantic to use custom Email class.

from typing import Optional, Annotated
import re

class BaseUser(BaseModel):
    model_config = ConfigDict(extra='forbid', hide_input_in_errors=True)

class UserUpdate(BaseUser):
    username: Optional[Annotated[str, StringConstraints(min_length=8, max_length=80)]] = None
    email: Optional[Email] = None

class UserCreate(BaseUser):
    username: Annotated[str, StringConstraints(min_length=8, max_length=80)]
    email: Email
    password: Annotated[str, StringConstraints(min_length=8, max_length=128)]

    @field_validator('username')
    def username_no_special_chars(cls, username):
        if not re.fullmatch(r'^[A-Za-z0-9_]+$', username):
            raise ValueError("Username must not contain special characters")
        return username


class UserListQuerySchema(BaseUser):
    page: Optional[int] = Field(default=1, ge=1)
    per_page: Optional[int] = Field(default=3, ge=1, lt=100)
