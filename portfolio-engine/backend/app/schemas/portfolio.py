from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PortfolioBase(BaseModel):
    name: str
    slug: str
    description: str | None = None


class PortfolioCreate(PortfolioBase):
    pass


class PortfolioUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None


class PortfolioResponse(PortfolioBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
