from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProjectTechnologyCreate(BaseModel):
    project_id: int
    name: str = Field(min_length=1, max_length=100)
    slug: str = Field(min_length=1, max_length=100)
    position: int = 0


class ProjectTechnologyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    slug: str | None = Field(default=None, min_length=1, max_length=100)
    position: int | None = None


class ProjectTechnologyResponse(BaseModel):
    id: int
    project_id: int
    name: str
    slug: str
    position: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
