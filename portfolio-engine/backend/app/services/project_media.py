from sqlalchemy.orm import Session

from app.models.project_media import ProjectMedia
from app.repositories.project import ProjectRepository
from app.repositories.project_media import ProjectMediaRepository
from app.schemas.project_media import (
    ProjectMediaCreate,
    ProjectMediaUpdate,
)


class ProjectNotFoundError(Exception):
    """Raised when a referenced project does not exist."""


class ProjectMediaService:
    def __init__(self, db: Session):
        self.repository = ProjectMediaRepository(db)
        self.project_repository = ProjectRepository(db)

    def create(self, data: ProjectMediaCreate) -> ProjectMedia:
        project = self.project_repository.get_by_id(
            data.project_id
        )

        if project is None:
            raise ProjectNotFoundError("Project not found")

        media = ProjectMedia(
            project_id=data.project_id,
            url=data.url,
            alt_text=data.alt_text,
            caption=data.caption,
            position=data.position,
        )

        return self.repository.create(media)

    def get_all(self) -> list[ProjectMedia]:
        return self.repository.get_all()

    def get_by_id(self, media_id: int) -> ProjectMedia | None:
        return self.repository.get_by_id(media_id)

    def get_by_project_id(
        self,
        project_id: int,
    ) -> list[ProjectMedia]:
        return self.repository.get_by_project_id(project_id)

    def update(
        self,
        media_id: int,
        data: ProjectMediaUpdate,
    ) -> ProjectMedia | None:
        media = self.repository.get_by_id(media_id)

        if media is None:
            return None

        update_data = data.model_dump(exclude_unset=True)

        if "project_id" in update_data:
            project = self.project_repository.get_by_id(
                update_data["project_id"]
            )

            if project is None:
                raise ProjectNotFoundError(
                    "Project not found"
                )

        for field, value in update_data.items():
            setattr(media, field, value)

        return self.repository.update(media)

    def delete(self, media_id: int) -> bool:
        media = self.repository.get_by_id(media_id)

        if media is None:
            return False

        self.repository.delete(media)
        return True
