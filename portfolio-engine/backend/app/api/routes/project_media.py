from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.schemas.project_media import (
    ProjectMediaCreate,
    ProjectMediaResponse,
    ProjectMediaUpdate,
)
from app.services.project_media import (
    ProjectMediaService,
    ProjectNotFoundError,
)


router = APIRouter(
    prefix="/api/project-media",
    tags=["Project Media"],
)


@router.post(
    "",
    response_model=ProjectMediaResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
def create_project_media(
    data: ProjectMediaCreate,
    db: Session = Depends(get_db),
):
    service = ProjectMediaService(db)

    try:
        return service.create(data)

    except ProjectNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[ProjectMediaResponse],
)
def get_project_media(
    db: Session = Depends(get_db),
):
    service = ProjectMediaService(db)
    return service.get_all()


@router.get(
    "/project/{project_id}",
    response_model=list[ProjectMediaResponse],
)
def get_project_media_by_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    service = ProjectMediaService(db)
    return service.get_by_project_id(project_id)


@router.get(
    "/{media_id}",
    response_model=ProjectMediaResponse,
)
def get_project_media_item(
    media_id: int,
    db: Session = Depends(get_db),
):
    service = ProjectMediaService(db)
    media = service.get_by_id(media_id)

    if media is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project media not found",
        )

    return media


@router.patch(
    "/{media_id}",
    response_model=ProjectMediaResponse,
    dependencies=[Depends(get_current_user)],
)
def update_project_media(
    media_id: int,
    data: ProjectMediaUpdate,
    db: Session = Depends(get_db),
):
    service = ProjectMediaService(db)

    try:
        media = service.update(media_id, data)

    except ProjectNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    if media is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project media not found",
        )

    return media


@router.delete(
    "/{media_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
def delete_project_media(
    media_id: int,
    db: Session = Depends(get_db),
):
    service = ProjectMediaService(db)

    if not service.delete(media_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project media not found",
        )
