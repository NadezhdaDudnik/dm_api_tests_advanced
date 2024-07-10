from typing import (
    Optional
)

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


class GeneralErrors(BaseModel):
    model_config = ConfigDict(extra="forbid")
    message: Optional[str] = Field(None, description='Client message')
