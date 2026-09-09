from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.certification import (
    CertificationCreate,
    CertificationResponse,
    CertificationUpdate,
)
from app.services.certification import (
    CertificationNotFoundError,
    CertificationService,
    PortfolioNotFoundError,
)


router = APIRouter(
    prefix="/api/certifications",
    tags=["Certifications"],
)


@router.post(
    "",
    response_model=CertificationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_certification(
    data: CertificationCreate,
    db: Session = Depends(get_db),
):
    service = CertificationService(db)

    try:
        return service.create(data)

    except PortfolioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[CertificationResponse],
)
def get_certifications(
    db: Session = Depends(get_db),
):
    service = CertificationService(db)

    return service.get_all()


@router.get(
    "/portfolio/{portfolio_id}",
    response_model=list[CertificationResponse],
)
def get_certifications_by_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
):
    service = CertificationService(db)

    try:
        return service.get_by_portfolio_id(portfolio_id)

    except PortfolioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{certification_id}",
    response_model=CertificationResponse,
)
def get_certification(
    certification_id: int,
    db: Session = Depends(get_db),
):
    service = CertificationService(db)

    try:
        return service.get_by_id(certification_id)

    except CertificationNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{certification_id}",
    response_model=CertificationResponse,
)
def update_certification(
    certification_id: int,
    data: CertificationUpdate,
    db: Session = Depends(get_db),
):
    service = CertificationService(db)

    try:
        return service.update(certification_id, data)

    except CertificationNotFoundError as exc:
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
    "/{certification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_certification(
    certification_id: int,
    db: Session = Depends(get_db),
):
    service = CertificationService(db)

    try:
        service.delete(certification_id)

    except CertificationNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
