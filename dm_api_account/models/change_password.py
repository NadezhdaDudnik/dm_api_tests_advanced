from typing import Optional
from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


class ChangePassword(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: str = Field(..., description="Логин")
    email: str = Field(..., description="E-mail")
    token: str = Field(None, description='Password reset token')
    old_password: str = Field(..., description="Old password")
    new_password: str = Field(..., description="New password")
