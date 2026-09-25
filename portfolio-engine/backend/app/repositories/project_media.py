from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project_media import ProjectMedia


class ProjectMediaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, media: ProjectMedia) -> ProjectMedia:
        self.db.add(media)
        self.db.commit()
        self.db.refresh(media)
        return media

    def get_all(self) -> list[ProjectMedia]:
        statement = select(ProjectMedia).order_by(
            ProjectMedia.position,
            ProjectMedia.id,
        )
        return list(self.db.scalars(statement).all())

    def get_by_id(self, media_id: int) -> ProjectMedia | None:
        return self.db.get(ProjectMedia, media_id)

    def get_by_project_id(self, project_id: int) -> list[ProjectMedia]:
        statement = (
            select(ProjectMedia)
            .where(ProjectMedia.project_id == project_id)
            .order_by(
                ProjectMedia.position,
                ProjectMedia.id,
            )
        )

        return list(self.db.scalars(statement).all())

    def update(self, media: ProjectMedia) -> ProjectMedia:
        self.db.commit()
        self.db.refresh(media)
        return media

    def delete(self, media: ProjectMedia) -> None:
        self.db.delete(media)
        self.db.commit()
