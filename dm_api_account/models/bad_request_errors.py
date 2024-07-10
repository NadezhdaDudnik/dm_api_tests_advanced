from typing import (
    Optional,
    Dict,
    List,
)

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


class Errors(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: str = Field(..., description="Логин")
    password: str = Field(..., description="Пароль")
    email: str = Field(..., description="E-mail")


class BadRequestErrors(BaseModel):
    model_config = ConfigDict(extra="forbid")
    message: Optional[str] = Field(None, description='Client message')
    invalid_properties: Optional[Dict[str, List[str]]] = Field(
        None, alias='invalidProperties',
        description='Key-value pairs of invalid request properties',
    )
