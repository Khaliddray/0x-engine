from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.certification import Certification
from app.models.education import Education
from app.models.experience import Experience
from app.models.portfolio_section import PortfolioSection
from app.models.project import Project
from app.models.project_media import ProjectMedia
from app.models.project_technology import ProjectTechnology
from app.models.resume import Resume
from app.models.skill import Skill
from app.models.social_link import SocialLink
from app.repositories.portfolio import PortfolioRepository
from app.schemas.public_portfolio import (
    PublicCertification,
    PublicEducation,
    PublicExperience,
    PublicPortfolioResponse,
    PublicPortfolioSection,
    PublicProject,
    PublicProjectMedia,
    PublicProjectTechnology,
    PublicResume,
    PublicSkill,
    PublicSocialLink,
)


class PublicPortfolioNotFoundError(Exception):
    """Raised when a public portfolio cannot be found."""


class PublicPortfolioService:
    def __init__(self, db: Session):
        self.db = db
        self.portfolio_repository = PortfolioRepository(db)

    def get_by_slug(
        self,
        slug: str,
    ) -> PublicPortfolioResponse:
        portfolio = self.portfolio_repository.get_by_slug(slug)

        if portfolio is None:
            raise PublicPortfolioNotFoundError(
                "Portfolio not found"
            )

        sections = self._get_sections(portfolio.id)
        projects = self._get_projects(portfolio.id)
        skills = self._get_skills(portfolio.id)
        experience = self._get_experience(portfolio.id)
        education = self._get_education(portfolio.id)
        certifications = self._get_certifications(portfolio.id)
        social_links = self._get_social_links(portfolio.id)
        resume = self._get_resume(portfolio.id)

        return PublicPortfolioResponse(
            name=portfolio.name,
            slug=portfolio.slug,
            description=portfolio.description,
            sections=sections,
            projects=projects,
            skills=skills,
            experience=experience,
            education=education,
            certifications=certifications,
            social_links=social_links,
            resume=resume,
        )

    def _get_sections(
        self,
        portfolio_id: int,
    ) -> list[PublicPortfolioSection]:
        statement = (
            select(PortfolioSection)
            .where(
                PortfolioSection.portfolio_id == portfolio_id,
                PortfolioSection.is_visible.is_(True),
            )
            .order_by(
                PortfolioSection.position,
                PortfolioSection.id,
            )
        )

        sections = self.db.scalars(statement).all()

        return [
            PublicPortfolioSection(
                title=section.title,
                slug=section.slug,
                type=section.type,
                content=section.content,
                position=section.position,
            )
            for section in sections
        ]

    def _get_projects(
        self,
        portfolio_id: int,
    ) -> list[PublicProject]:
        statement = (
            select(Project)
            .where(Project.portfolio_id == portfolio_id)
            .order_by(Project.id)
        )

        projects = self.db.scalars(statement).all()

        result = []

        for project in projects:
            technologies = self._get_project_technologies(
                project.id
            )
            media = self._get_project_media(project.id)

            result.append(
                PublicProject(
                    id=project.id,
                    title=project.title,
                    slug=project.slug,
                    description=project.description,
                    github_url=project.github_url,
                    live_url=project.live_url,
                    is_featured=project.is_featured,
                    technologies=technologies,
                    media=media,
                )
            )

        return result

    def _get_project_technologies(
        self,
        project_id: int,
    ) -> list[PublicProjectTechnology]:
        statement = (
            select(ProjectTechnology)
            .where(ProjectTechnology.project_id == project_id)
            .order_by(
                ProjectTechnology.position,
                ProjectTechnology.id,
            )
        )

        technologies = self.db.scalars(statement).all()

        return [
            PublicProjectTechnology(
                name=technology.name,
                slug=technology.slug,
                position=technology.position,
            )
            for technology in technologies
        ]

    def _get_project_media(
        self,
        project_id: int,
    ) -> list[PublicProjectMedia]:
        statement = (
            select(ProjectMedia)
            .where(ProjectMedia.project_id == project_id)
            .order_by(
                ProjectMedia.position,
                ProjectMedia.id,
            )
        )

        media_items = self.db.scalars(statement).all()

        return [
            PublicProjectMedia(
                url=media.url,
                alt_text=media.alt_text,
                caption=media.caption,
                position=media.position,
            )
            for media in media_items
        ]

    def _get_skills(
        self,
        portfolio_id: int,
    ) -> list[PublicSkill]:
        statement = (
            select(Skill)
            .where(
                Skill.portfolio_id == portfolio_id,
                Skill.is_visible.is_(True),
            )
            .order_by(
                Skill.position,
                Skill.id,
            )
        )

        skills = self.db.scalars(statement).all()

        return [
            PublicSkill(
                name=skill.name,
                slug=skill.slug,
                category=skill.category,
                proficiency=skill.proficiency,
                position=skill.position,
            )
            for skill in skills
        ]

    def _get_experience(
        self,
        portfolio_id: int,
    ) -> list[PublicExperience]:
        statement = (
            select(Experience)
            .where(
                Experience.portfolio_id == portfolio_id,
                Experience.is_visible.is_(True),
            )
            .order_by(
                Experience.position,
                Experience.id,
            )
        )

        experiences = self.db.scalars(statement).all()

        return [
            PublicExperience(
                company=item.company,
                role=item.role,
                employment_type=item.employment_type,
                location=item.location,
                start_date=item.start_date,
                end_date=item.end_date,
                description=item.description,
                position=item.position,
            )
            for item in experiences
        ]

    def _get_education(
        self,
        portfolio_id: int,
    ) -> list[PublicEducation]:
        statement = (
            select(Education)
            .where(
                Education.portfolio_id == portfolio_id,
                Education.is_visible.is_(True),
            )
            .order_by(
                Education.position,
                Education.id,
            )
        )

        education_records = self.db.scalars(statement).all()

        return [
            PublicEducation(
                institution=item.institution,
                degree=item.degree,
                field_of_study=item.field_of_study,
                location=item.location,
                start_date=item.start_date,
                end_date=item.end_date,
                description=item.description,
                position=item.position,
            )
            for item in education_records
        ]

    def _get_certifications(
        self,
        portfolio_id: int,
    ) -> list[PublicCertification]:
        statement = (
            select(Certification)
            .where(
                Certification.portfolio_id == portfolio_id,
                Certification.is_visible.is_(True),
            )
            .order_by(
                Certification.position,
                Certification.id,
            )
        )

        certifications = self.db.scalars(statement).all()

        return [
            PublicCertification(
                name=item.name,
                issuer=item.issuer,
                credential_id=item.credential_id,
                credential_url=item.credential_url,
                issue_date=item.issue_date,
                expiration_date=item.expiration_date,
                description=item.description,
                position=item.position,
            )
            for item in certifications
        ]

    def _get_social_links(
        self,
        portfolio_id: int,
    ) -> list[PublicSocialLink]:
        statement = (
            select(SocialLink)
            .where(
                SocialLink.portfolio_id == portfolio_id,
                SocialLink.is_visible.is_(True),
            )
            .order_by(
                SocialLink.position,
                SocialLink.id,
            )
        )

        social_links = self.db.scalars(statement).all()

        return [
            PublicSocialLink(
                platform=item.platform,
                url=item.url,
                label=item.label,
                position=item.position,
            )
            for item in social_links
        ]

    def _get_resume(
        self,
        portfolio_id: int,
    ) -> PublicResume | None:
        statement = (
            select(Resume)
            .where(
                Resume.portfolio_id == portfolio_id,
                Resume.is_primary.is_(True),
                Resume.is_visible.is_(True),
            )
            .order_by(Resume.id)
        )

        resume = self.db.scalar(statement)

        if resume is None:
            return None

        return PublicResume(
            title=resume.title,
            file_url=resume.file_url,
            version=resume.version,
            description=resume.description,
        )
