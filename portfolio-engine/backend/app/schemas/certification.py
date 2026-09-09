from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class CertificationBase(BaseModel):
    portfolio_id: int
    name: str
    issuer: str
    credential_id: str | None = None
    credential_url: str | None = None
    issue_date: date
    expiration_date: date | None = None
    description: str | None = None
    position: int = 0
    is_visible: bool = True


class CertificationCreate(CertificationBase):
    pass


class CertificationUpdate(BaseModel):
    portfolio_id: int | None = Field(
        default=None,
        description="Portfolio ID to move the certification to.",
    )
    name: str | None = Field(
        default=None,
        description="Name of the certification.",
    )
    issuer: str | None = Field(
        default=None,
        description="Organization that issued the certification.",
    )
    credential_id: str | None = Field(
        default=None,
        description="Certificate or credential ID.",
    )
    credential_url: str | None = Field(
        default=None,
        description="URL where the credential can be verified.",
    )
    issue_date: date | None = Field(
        default=None,
        description="Date the certification was issued.",
    )
    expiration_date: date | None = Field(
        default=None,
        description="Expiration date, if applicable.",
    )
    description: str | None = Field(
        default=None,
        description="Additional information about the certification.",
    )
    position: int | None = Field(
        default=None,
        description="Display order of the certification.",
    )
    is_visible: bool | None = Field(
        default=None,
        description="Whether the certification is visible.",
    )


class CertificationResponse(CertificationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
