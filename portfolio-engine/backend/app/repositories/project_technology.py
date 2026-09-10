from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project_technology import ProjectTechnology


class ProjectTechnologyRepository:
    def create(
        self,
        db: Session,
        project_technology: ProjectTechnology,
    ) -> ProjectTechnology:
        db.add(project_technology)
        db.commit()
        db.refresh(project_technology)

        return project_technology

    def get_all(
        self,
        db: Session,
    ) -> list[ProjectTechnology]:
        statement = select(ProjectTechnology).order_by(
            ProjectTechnology.position,
            ProjectTechnology.id,
        )

        return list(db.scalars(statement).all())

    def get_by_id(
        self,
        db: Session,
        technology_id: int,
    ) -> ProjectTechnology | None:
        statement = select(ProjectTechnology).where(
            ProjectTechnology.id == technology_id
        )

        return db.scalar(statement)

    def get_by_project_id(
        self,
        db: Session,
        project_id: int,
    ) -> list[ProjectTechnology]:
        statement = (
            select(ProjectTechnology)
            .where(ProjectTechnology.project_id == project_id)
            .order_by(
                ProjectTechnology.position,
                ProjectTechnology.id,
            )
        )

        return list(db.scalars(statement).all())

    def update(
        self,
        db: Session,
        project_technology: ProjectTechnology,
    ) -> ProjectTechnology:
        db.commit()
        db.refresh(project_technology)

        return project_technology

    def delete(
        self,
        db: Session,
        project_technology: ProjectTechnology,
    ) -> None:
        db.delete(project_technology)
        db.commit()
