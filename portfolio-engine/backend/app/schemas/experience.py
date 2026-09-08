from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class ExperienceBase(BaseModel):
    portfolio_id: int
    company: str
    role: str
    employment_type: str | None = None
    location: str | None = None
    start_date: date
    end_date: date | None = None
    description: str | None = None
    position: int = 0
    is_visible: bool = True


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceUpdate(BaseModel):
    portfolio_id: int | None = Field(
        default=None,
        description="Portfolio ID to move the experience to.",
    )
    company: str | None = Field(
        default=None,
        description="Company or organization name.",
    )
    role: str | None = Field(
        default=None,
        description="Job or professional role.",
    )
    employment_type: str | None = Field(
        default=None,
        description="Employment type, such as Full-time, Part-time, or Internship.",
    )
    location: str | None = Field(
        default=None,
        description="Work location.",
    )
    start_date: date | None = Field(
        default=None,
        description="Experience start date.",
    )
    end_date: date | None = Field(
        default=None,
        description="Experience end date. Leave null for an ongoing role.",
    )
    description: str | None = Field(
        default=None,
        description="Description of the experience.",
    )
    position: int | None = Field(
        default=None,
        description="Display order of the experience.",
    )
    is_visible: bool | None = Field(
        default=None,
        description="Whether the experience is visible.",
    )


class ExperienceResponse(ExperienceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
