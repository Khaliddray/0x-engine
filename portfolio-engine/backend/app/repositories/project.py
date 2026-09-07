from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, project: Project) -> Project:
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_all(self) -> list[Project]:
        statement = select(Project).order_by(Project.id)
        return list(self.db.scalars(statement).all())

    def get_by_id(self, project_id: int) -> Project | None:
        statement = select(Project).where(Project.id == project_id)
        return self.db.scalar(statement)

    def get_by_slug(self, slug: str) -> Project | None:
        statement = select(Project).where(Project.slug == slug)
        return self.db.scalar(statement)

    def get_by_portfolio_id(self, portfolio_id: int) -> list[Project]:
        statement = (
            select(Project)
            .where(Project.portfolio_id == portfolio_id)
            .order_by(Project.id)
        )

        return list(self.db.scalars(statement).all())

    def update(self, project: Project) -> Project:
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, project: Project) -> None:
        self.db.delete(project)
        self.db.commit()
