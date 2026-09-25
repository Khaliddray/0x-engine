from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProjectMediaBase(BaseModel):
    project_id: int
    url: str
    alt_text: str | None = None
    caption: str | None = None
    position: int = 0


class ProjectMediaCreate(ProjectMediaBase):
    pass


class ProjectMediaUpdate(BaseModel):
    project_id: int | None = Field(
        default=None,
        description="Project ID to move the media item to.",
    )

    url: str | None = Field(
        default=None,
        description="URL of the project media.",
    )

    alt_text: str | None = Field(
        default=None,
        description="Alternative text for accessibility.",
    )

    caption: str | None = Field(
        default=None,
        description="Optional media caption.",
    )

    position: int | None = Field(
        default=None,
        description="Display order of the media item.",
    )


class ProjectMediaResponse(ProjectMediaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
