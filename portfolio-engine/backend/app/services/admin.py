from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.certification import Certification
from app.models.education import Education
from app.models.experience import Experience
from app.models.portfolio import Portfolio
from app.models.portfolio_section import PortfolioSection
from app.models.project import Project
from app.models.project_media import ProjectMedia
from app.models.project_technology import ProjectTechnology
from app.models.resume import Resume
from app.models.skill import Skill
from app.models.social_link import SocialLink
from app.models.user import User
from app.schemas.admin import AdminOverviewResponse


class AdminService:
    def __init__(self, db: Session):
        self.db = db

    def get_overview(self) -> AdminOverviewResponse:
        total_portfolios = self.db.scalar(select(func.count(Portfolio.id))) or 0
        total_projects = self.db.scalar(select(func.count(Project.id))) or 0
        total_featured_projects = (
            self.db.scalar(
                select(func.count(Project.id)).where(Project.is_featured.is_(True))
            )
            or 0
        )
        total_sections = (
            self.db.scalar(select(func.count(PortfolioSection.id))) or 0
        )
        total_skills = self.db.scalar(select(func.count(Skill.id))) or 0
        total_experiences = (
            self.db.scalar(select(func.count(Experience.id))) or 0
        )
        total_education = self.db.scalar(select(func.count(Education.id))) or 0
        total_certifications = (
            self.db.scalar(select(func.count(Certification.id))) or 0
        )
        total_social_links = (
            self.db.scalar(select(func.count(SocialLink.id))) or 0
        )
        total_resumes = self.db.scalar(select(func.count(Resume.id))) or 0
        total_project_media = (
            self.db.scalar(select(func.count(ProjectMedia.id))) or 0
        )
        total_project_technologies = (
            self.db.scalar(select(func.count(ProjectTechnology.id))) or 0
        )
        total_users = self.db.scalar(select(func.count(User.id))) or 0

        return AdminOverviewResponse(
            total_portfolios=total_portfolios,
            total_projects=total_projects,
            total_featured_projects=total_featured_projects,
            total_sections=total_sections,
            total_skills=total_skills,
            total_experiences=total_experiences,
            total_education=total_education,
            total_certifications=total_certifications,
            total_social_links=total_social_links,
            total_resumes=total_resumes,
            total_project_media=total_project_media,
            total_project_technologies=total_project_technologies,
            total_users=total_users,
        )
