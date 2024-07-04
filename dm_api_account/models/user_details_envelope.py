from datetime import datetime
from enum import Enum

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from typing import (
    List,
    Optional,
)


class UserRole(str, Enum):
    GUEST = "Guest"
    PLAYER = "Player"
    ADMINISTRATOR = "Administrator"
    NANNY_MODERATOR = "NannyModerator"
    REGULAR_MODERATOR = "RegularModerator"
    SENIOR_MODERATOR = "SeniorModerator"


class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int


class PagingSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")
    postsPerPage: int
    commentsPerPage: int
    topicsPerPage: int
    messagesPerPage: int
    entitiesPerPage: int


class BbParseMode(str, Enum):
    common = 'Common'
    info = 'Info'
    post = 'Post'
    chat = 'Chat'


class ColorSchema(str, Enum):
    modern = 'Modern'
    pale = 'Pale'
    classic = 'Classic'
    classic_pale = 'ClassicPale'
    night = 'Night'


class InfoBbText(BaseModel):
    model_config = ConfigDict(extra="forbid")

    value: Optional[str] = Field(None, description='Text')
    parse_mode: Optional[BbParseMode] = Field(None, alias='parseMode')


class UserSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    color_schema: Optional[ColorSchema] = Field(None, alias='colorSchema')
    nanny_greetings_message: Optional[str] = Field(
        None,
        alias='nannyGreetingsMessage'
    )
    paging: Optional[PagingSettings] = None


class UserDetails(BaseModel):
    login: str
    roles: List[UserRole]
    mediumPictureUrl: str = Field(None, serialization_alias="mediumPictureUrl")
    smallPictureUrl: str = Field(None, serialization_alias="smallPictureUrl")
    status: str = Field(None, alias="status")
    rating: Rating
    online: datetime = Field(None, alias="online")
    name: str = Field(None, alias="name")
    location: str = Field(None, alias="location")
    registration: datetime = Field(None, alias="registration")
    icq: str = Field(None, alias="icq")
    skype: str = Field(None, alias="skype")
    originalPictureUrl: str = Field(None, serialization_alias="originalPictureUrl")
    info: Optional[InfoBbText] = Field(None)
    settings: Optional[UserSettings] = Field(None)


class UserDetailsEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resource: Optional[UserDetails] = None
    metadata: Optional[str] = None
