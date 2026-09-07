from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProjectBase(BaseModel):
    portfolio_id: int
    title: str
    slug: str
    description: str | None = None
    github_url: str | None = None
    live_url: str | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    portfolio_id: int | None = Field(
        default=None,
        description="Portfolio ID to move the project to.",
    )

    title: str | None = Field(
        default=None,
        description="Project title.",
    )

    slug: str | None = Field(
        default=None,
        description="Unique project slug.",
    )

    description: str | None = Field(
        default=None,
        description="Project description.",
    )

    github_url: str | None = Field(
        default=None,
        description="GitHub repository URL.",
    )

    live_url: str | None = Field(
        default=None,
        description="Live project URL.",
    )


class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
