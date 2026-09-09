from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class EducationBase(BaseModel):
    portfolio_id: int
    institution: str
    degree: str
    field_of_study: str | None = None
    location: str | None = None
    start_date: date
    end_date: date | None = None
    description: str | None = None
    position: int = 0
    is_visible: bool = True


class EducationCreate(EducationBase):
    pass


class EducationUpdate(BaseModel):
    portfolio_id: int | None = Field(
        default=None,
        description="Portfolio ID to move the education record to.",
    )
    institution: str | None = Field(
        default=None,
        description="Name of the educational institution.",
    )
    degree: str | None = Field(
        default=None,
        description="Degree or qualification obtained.",
    )
    field_of_study: str | None = Field(
        default=None,
        description="Field or course of study.",
    )
    location: str | None = Field(
        default=None,
        description="Location of the institution.",
    )
    start_date: date | None = Field(
        default=None,
        description="Education start date.",
    )
    end_date: date | None = Field(
        default=None,
        description="Education end date. Leave null for ongoing education.",
    )
    description: str | None = Field(
        default=None,
        description="Description of the education.",
    )
    position: int | None = Field(
        default=None,
        description="Display order of the education.",
    )
    is_visible: bool | None = Field(
        default=None,
        description="Whether the education is visible.",
    )


class EducationResponse(EducationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
