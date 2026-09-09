from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SocialLinkBase(BaseModel):
    portfolio_id: int
    platform: str
    url: str
    label: str | None = None
    position: int = 0
    is_visible: bool = True


class SocialLinkCreate(SocialLinkBase):
    pass


class SocialLinkUpdate(BaseModel):
    portfolio_id: int | None = Field(
        default=None,
        description="Portfolio ID to move the social link to.",
    )
    platform: str | None = Field(
        default=None,
        description="Social platform name, such as GitHub or LinkedIn.",
    )
    url: str | None = Field(
        default=None,
        description="URL of the social profile.",
    )
    label: str | None = Field(
        default=None,
        description="Optional display label for the social link.",
    )
    position: int | None = Field(
        default=None,
        description="Display order of the social link.",
    )
    is_visible: bool | None = Field(
        default=None,
        description="Whether the social link is publicly visible.",
    )


class SocialLinkResponse(SocialLinkBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
