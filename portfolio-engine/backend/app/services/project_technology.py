from sqlalchemy.orm import Session

from app.models.project_technology import ProjectTechnology
from app.repositories.project_technology import ProjectTechnologyRepository


class ProjectTechnologyService:
    def __init__(self) -> None:
        self.repository = ProjectTechnologyRepository()

    def create(
        self,
        db: Session,
        project_id: int,
        name: str,
        slug: str,
        position: int = 0,
    ) -> ProjectTechnology:
        project_technology = ProjectTechnology(
            project_id=project_id,
            name=name,
            slug=slug,
            position=position,
        )

        return self.repository.create(db, project_technology)

    def get_all(
        self,
        db: Session,
    ) -> list[ProjectTechnology]:
        return self.repository.get_all(db)

    def get_by_id(
        self,
        db: Session,
        technology_id: int,
    ) -> ProjectTechnology | None:
        return self.repository.get_by_id(db, technology_id)

    def get_by_project_id(
        self,
        db: Session,
        project_id: int,
    ) -> list[ProjectTechnology]:
        return self.repository.get_by_project_id(db, project_id)

    def update(
        self,
        db: Session,
        project_technology: ProjectTechnology,
        data: dict,
    ) -> ProjectTechnology:
        for field, value in data.items():
            setattr(project_technology, field, value)

        return self.repository.update(db, project_technology)

    def delete(
        self,
        db: Session,
        project_technology: ProjectTechnology,
    ) -> None:
        self.repository.delete(db, project_technology)
