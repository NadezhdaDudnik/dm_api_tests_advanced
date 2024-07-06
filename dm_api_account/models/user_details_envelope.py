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
    Any,
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
    postsPerPage: int = Field(None, serialization_alias='postsPerPage')
    commentsPerPage: int = Field(None, serialization_alias='commentsPerPage')
    topicsPerPage: int = Field(None, serialization_alias='topicsPerPage')
    messagesPerPage: int = Field(None, serialization_alias='messagesPerPage')
    entitiesPerPage: int = Field(None, serialization_alias='entitiesPerPage')


class BbParseMode(str, Enum):
    COMMON = 'Common'
    INFO = 'Info'
    POST = 'Post'
    CHAT = 'Chat'


class ColorSchema(str, Enum):
    MODERN = 'Modern'
    PALE = 'Pale'
    CLASSIC = 'Classic'
    CLASSIC_PALE = 'ClassicPale'
    NIGHT = 'Night'


class InfoBbText(BaseModel):
    model_config = ConfigDict(extra="forbid")
    value: Optional[str] = Field(None, description='Text')
    parse_mode: Optional[BbParseMode] = Field(None, alias='parseMode')


class UserSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    colorSchema: Optional[ColorSchema] = Field(None, serialization_alias='colorSchema')
    nannyGreetingsMessage: Optional[str] = Field(None, serialization_alias='nannyGreetingsMessage')
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
    #info: InfoBbText
    info: Any = Field(None)
    settings: Optional[UserSettings] = Field(None)


class UserDetailsEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resource: Optional[UserDetails] = None
    metadata: Optional[Any] = None
