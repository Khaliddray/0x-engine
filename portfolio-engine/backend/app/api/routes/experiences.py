from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.experience import (
    ExperienceCreate,
    ExperienceResponse,
    ExperienceUpdate,
)
from app.services.experience import (
    ExperienceNotFoundError,
    ExperienceService,
    PortfolioNotFoundError,
)


router = APIRouter(
    prefix="/api/experiences",
    tags=["Experiences"],
)


@router.post(
    "",
    response_model=ExperienceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_experience(
    data: ExperienceCreate,
    db: Session = Depends(get_db),
):
    service = ExperienceService(db)

    try:
        return service.create(data)

    except PortfolioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[ExperienceResponse],
)
def get_experiences(
    db: Session = Depends(get_db),
):
    service = ExperienceService(db)
    return service.get_all()


@router.get(
    "/portfolio/{portfolio_id}",
    response_model=list[ExperienceResponse],
)
def get_experiences_by_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
):
    service = ExperienceService(db)

    try:
        return service.get_by_portfolio_id(portfolio_id)

    except PortfolioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{experience_id}",
    response_model=ExperienceResponse,
)
def get_experience(
    experience_id: int,
    db: Session = Depends(get_db),
):
    service = ExperienceService(db)

    try:
        return service.get_by_id(experience_id)

    except ExperienceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{experience_id}",
    response_model=ExperienceResponse,
)
def update_experience(
    experience_id: int,
    data: ExperienceUpdate,
    db: Session = Depends(get_db),
):
    service = ExperienceService(db)

    try:
        return service.update(experience_id, data)

    except ExperienceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except PortfolioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{experience_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_experience(
    experience_id: int,
    db: Session = Depends(get_db),
):
    service = ExperienceService(db)

    try:
        service.delete(experience_id)

    except ExperienceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
