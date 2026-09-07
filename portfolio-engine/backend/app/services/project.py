from sqlalchemy.orm import Session

from app.models.project import Project
from app.repositories.portfolio import PortfolioRepository
from app.repositories.project import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate


class PortfolioNotFoundError(Exception):
    """Raised when a referenced portfolio does not exist."""


class ProjectSlugExistsError(Exception):
    """Raised when a project slug is already in use."""


class ProjectService:
    def __init__(self, db: Session):
        self.repository = ProjectRepository(db)
        self.portfolio_repository = PortfolioRepository(db)

    def create(self, data: ProjectCreate) -> Project:
        portfolio = self.portfolio_repository.get_by_id(
            data.portfolio_id
        )

        if portfolio is None:
            raise PortfolioNotFoundError("Portfolio not found")

        existing_project = self.repository.get_by_slug(data.slug)

        if existing_project is not None:
            raise ProjectSlugExistsError(
                "Project slug already exists"
            )

        project = Project(
            portfolio_id=data.portfolio_id,
            title=data.title,
            slug=data.slug,
            description=data.description,
            github_url=data.github_url,
            live_url=data.live_url,
        )

        return self.repository.create(project)

    def get_all(self) -> list[Project]:
        return self.repository.get_all()

    def get_by_id(self, project_id: int) -> Project | None:
        return self.repository.get_by_id(project_id)

    def get_by_portfolio_id(self, portfolio_id: int) -> list[Project]:
        return self.repository.get_by_portfolio_id(portfolio_id)

    def update(
        self,
        project_id: int,
        data: ProjectUpdate,
    ) -> Project | None:
        project = self.repository.get_by_id(project_id)

        if project is None:
            return None

        update_data = data.model_dump(exclude_unset=True)

        if "portfolio_id" in update_data:
            portfolio = self.portfolio_repository.get_by_id(
                update_data["portfolio_id"]
            )

            if portfolio is None:
                raise PortfolioNotFoundError(
                    "Portfolio not found"
                )

        if "slug" in update_data:
            existing_project = self.repository.get_by_slug(
                update_data["slug"]
            )

            if (
                existing_project is not None
                and existing_project.id != project_id
            ):
                raise ProjectSlugExistsError(
                    "Project slug already exists"
                )

        for field, value in update_data.items():
            setattr(project, field, value)

        return self.repository.update(project)

    def delete(self, project_id: int) -> bool:
        project = self.repository.get_by_id(project_id)

        if project is None:
            return False

        self.repository.delete(project)
        return True
