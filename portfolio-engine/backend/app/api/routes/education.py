from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.education import (
    EducationCreate,
    EducationResponse,
    EducationUpdate,
)
from app.services.education import (
    EducationNotFoundError,
    EducationService,
    PortfolioNotFoundError,
)


router = APIRouter(
    prefix="/api/education",
    tags=["Education"],
)


@router.post(
    "",
    response_model=EducationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_education(
    data: EducationCreate,
    db: Session = Depends(get_db),
):
    service = EducationService(db)

    try:
        return service.create(data)

    except PortfolioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[EducationResponse],
)
def get_education(
    db: Session = Depends(get_db),
):
    service = EducationService(db)

    return service.get_all()


@router.get(
    "/portfolio/{portfolio_id}",
    response_model=list[EducationResponse],
)
def get_education_by_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
):
    service = EducationService(db)

    try:
        return service.get_by_portfolio_id(portfolio_id)

    except PortfolioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{education_id}",
    response_model=EducationResponse,
)
def get_education_record(
    education_id: int,
    db: Session = Depends(get_db),
):
    service = EducationService(db)

    try:
        return service.get_by_id(education_id)

    except EducationNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{education_id}",
    response_model=EducationResponse,
)
def update_education(
    education_id: int,
    data: EducationUpdate,
    db: Session = Depends(get_db),
):
    service = EducationService(db)

    try:
        return service.update(education_id, data)

    except EducationNotFoundError as exc:
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
    "/{education_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_education(
    education_id: int,
    db: Session = Depends(get_db),
):
    service = EducationService(db)

    try:
        service.delete(education_id)

    except EducationNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
