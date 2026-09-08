from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.portfolio_section import (
    PortfolioSectionCreate,
    PortfolioSectionResponse,
    PortfolioSectionUpdate,
)
from app.services.portfolio_section import (
    PortfolioNotFoundError,
    PortfolioSectionNotFoundError,
    PortfolioSectionService,
    PortfolioSectionSlugExistsError,
)


router = APIRouter(
    prefix="/api/sections",
    tags=["Portfolio Sections"],
)


@router.post(
    "",
    response_model=PortfolioSectionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_section(
    data: PortfolioSectionCreate,
    db: Session = Depends(get_db),
):
    service = PortfolioSectionService(db)

    try:
        return service.create(data)
    except PortfolioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except PortfolioSectionSlugExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[PortfolioSectionResponse],
)
def get_sections(
    db: Session = Depends(get_db),
):
    service = PortfolioSectionService(db)
    return service.get_all()


@router.get(
    "/portfolio/{portfolio_id}",
    response_model=list[PortfolioSectionResponse],
)
def get_sections_by_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
):
    service = PortfolioSectionService(db)

    try:
        return service.get_by_portfolio_id(portfolio_id)
    except PortfolioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{section_id}",
    response_model=PortfolioSectionResponse,
)
def get_section(
    section_id: int,
    db: Session = Depends(get_db),
):
    service = PortfolioSectionService(db)

    try:
        return service.get_by_id(section_id)
    except PortfolioSectionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{section_id}",
    response_model=PortfolioSectionResponse,
)
def update_section(
    section_id: int,
    data: PortfolioSectionUpdate,
    db: Session = Depends(get_db),
):
    service = PortfolioSectionService(db)

    try:
        return service.update(section_id, data)
    except PortfolioSectionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except PortfolioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except PortfolioSectionSlugExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{section_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_section(
    section_id: int,
    db: Session = Depends(get_db),
):
    service = PortfolioSectionService(db)

    try:
        service.delete(section_id)
    except PortfolioSectionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
