from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.project_technology import (
    ProjectTechnologyCreate,
    ProjectTechnologyResponse,
    ProjectTechnologyUpdate,
)
from app.services.project_technology import ProjectTechnologyService


router = APIRouter(
    prefix="/api/project-technologies",
    tags=["Project Technologies"],
)

service = ProjectTechnologyService()


@router.post(
    "",
    response_model=ProjectTechnologyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project_technology(
    data: ProjectTechnologyCreate,
    db: Session = Depends(get_db),
):
    return service.create(
        db=db,
        project_id=data.project_id,
        name=data.name,
        slug=data.slug,
        position=data.position,
    )


@router.get(
    "",
    response_model=list[ProjectTechnologyResponse],
)
def get_project_technologies(
    db: Session = Depends(get_db),
):
    return service.get_all(db)


@router.get(
    "/project/{project_id}",
    response_model=list[ProjectTechnologyResponse],
)
def get_project_technologies_by_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    return service.get_by_project_id(db, project_id)


@router.get(
    "/{technology_id}",
    response_model=ProjectTechnologyResponse,
)
def get_project_technology(
    technology_id: int,
    db: Session = Depends(get_db),
):
    project_technology = service.get_by_id(db, technology_id)

    if project_technology is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project technology not found",
        )

    return project_technology


@router.patch(
    "/{technology_id}",
    response_model=ProjectTechnologyResponse,
)
def update_project_technology(
    technology_id: int,
    data: ProjectTechnologyUpdate,
    db: Session = Depends(get_db),
):
    project_technology = service.get_by_id(db, technology_id)

    if project_technology is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project technology not found",
        )

    update_data = data.model_dump(exclude_unset=True)

    return service.update(
        db=db,
        project_technology=project_technology,
        data=update_data,
    )


@router.delete(
    "/{technology_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project_technology(
    technology_id: int,
    db: Session = Depends(get_db),
):
    project_technology = service.get_by_id(db, technology_id)

    if project_technology is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project technology not found",
        )

    service.delete(db, project_technology)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
