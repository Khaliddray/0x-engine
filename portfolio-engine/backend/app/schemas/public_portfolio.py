from datetime import date

from pydantic import BaseModel


class PublicPortfolioSection(BaseModel):
    title: str
    slug: str
    type: str
    content: str | None = None
    position: int


class PublicProjectTechnology(BaseModel):
    name: str
    slug: str
    position: int


class PublicProjectMedia(BaseModel):
    url: str
    alt_text: str | None = None
    caption: str | None = None
    position: int


class PublicProject(BaseModel):
    id: int
    title: str
    slug: str
    description: str | None = None
    github_url: str | None = None
    live_url: str | None = None
    is_featured: bool
    technologies: list[PublicProjectTechnology]
    media: list[PublicProjectMedia]


class PublicSkill(BaseModel):
    name: str
    slug: str
    category: str | None = None
    proficiency: str | None = None
    position: int


class PublicExperience(BaseModel):
    company: str
    role: str
    employment_type: str | None = None
    location: str | None = None
    start_date: date
    end_date: date | None = None
    description: str | None = None
    position: int


class PublicEducation(BaseModel):
    institution: str
    degree: str
    field_of_study: str | None = None
    location: str | None = None
    start_date: date
    end_date: date | None = None
    description: str | None = None
    position: int


class PublicCertification(BaseModel):
    name: str
    issuer: str
    credential_id: str | None = None
    credential_url: str | None = None
    issue_date: date
    expiration_date: date | None = None
    description: str | None = None
    position: int


class PublicSocialLink(BaseModel):
    platform: str
    url: str
    label: str | None = None
    position: int


class PublicResume(BaseModel):
    title: str
    file_url: str
    version: str
    description: str | None = None


class PublicPortfolioResponse(BaseModel):
    name: str
    slug: str
    description: str | None = None
    sections: list[PublicPortfolioSection]
    projects: list[PublicProject]
    skills: list[PublicSkill]
    experience: list[PublicExperience]
    education: list[PublicEducation]
    certifications: list[PublicCertification]
    social_links: list[PublicSocialLink]
    resume: PublicResume | None = None
