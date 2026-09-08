from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PortfolioSectionBase(BaseModel):
    portfolio_id: int
    title: str
    slug: str
    type: str
    content: str | None = None
    position: int = 0
    is_visible: bool = True


class PortfolioSectionCreate(PortfolioSectionBase):
    pass


class PortfolioSectionUpdate(BaseModel):
    portfolio_id: int | None = Field(
        default=None,
        description="Portfolio ID to move the section to.",
    )
    title: str | None = Field(
        default=None,
        description="Section title.",
    )
    slug: str | None = Field(
        default=None,
        description="Unique section slug.",
    )
    type: str | None = Field(
        default=None,
        description="Section type.",
    )
    content: str | None = Field(
        default=None,
        description="Section content.",
    )
    position: int | None = Field(
        default=None,
        description="Display order of the section.",
    )
    is_visible: bool | None = Field(
        default=None,
        description="Whether the section is visible.",
    )


class PortfolioSectionResponse(PortfolioSectionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
