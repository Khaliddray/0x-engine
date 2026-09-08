from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SkillBase(BaseModel):
    portfolio_id: int
    name: str
    slug: str
    category: str | None = None
    proficiency: str | None = None
    position: int = 0
    is_visible: bool = True


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    portfolio_id: int | None = Field(
        default=None,
        description="Portfolio ID to move the skill to.",
    )
    name: str | None = Field(
        default=None,
        description="Skill name.",
    )
    slug: str | None = Field(
        default=None,
        description="Unique skill slug.",
    )
    category: str | None = Field(
        default=None,
        description="Skill category.",
    )
    proficiency: str | None = Field(
        default=None,
        description="Skill proficiency level.",
    )
    position: int | None = Field(
        default=None,
        description="Display order of the skill.",
    )
    is_visible: bool | None = Field(
        default=None,
        description="Whether the skill is visible.",
    )


class SkillResponse(SkillBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
