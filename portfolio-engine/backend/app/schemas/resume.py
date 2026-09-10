from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ResumeBase(BaseModel):
    portfolio_id: int
    title: str
    file_url: str
    version: str
    description: str | None = None
    is_primary: bool = False
    is_visible: bool = True


class ResumeCreate(ResumeBase):
    pass


class ResumeUpdate(BaseModel):
    portfolio_id: int | None = Field(
        default=None,
        description="Portfolio ID to move the resume to.",
    )
    title: str | None = Field(
        default=None,
        description="Resume title.",
    )
    file_url: str | None = Field(
        default=None,
        description="URL of the resume file.",
    )
    version: str | None = Field(
        default=None,
        description="Resume version identifier.",
    )
    description: str | None = Field(
        default=None,
        description="Optional description of the resume.",
    )
    is_primary: bool | None = Field(
        default=None,
        description="Whether this is the primary resume.",
    )
    is_visible: bool | None = Field(
        default=None,
        description="Whether the resume is publicly visible.",
    )


class ResumeResponse(ResumeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
