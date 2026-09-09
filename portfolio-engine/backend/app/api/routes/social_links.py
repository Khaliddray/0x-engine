from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.social_link import (
    SocialLinkCreate,
    SocialLinkResponse,
    SocialLinkUpdate,
)
from app.services.social_link import (
    PortfolioNotFoundError,
    SocialLinkNotFoundError,
    SocialLinkService,
)


router = APIRouter(
    prefix="/api/social-links",
    tags=["Social Links"],
)


@router.post(
    "",
    response_model=SocialLinkResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_social_link(
    data: SocialLinkCreate,
    db: Session = Depends(get_db),
):
    service = SocialLinkService(db)

    try:
        return service.create(data)

    except PortfolioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[SocialLinkResponse],
)
def get_social_links(
    db: Session = Depends(get_db),
):
    service = SocialLinkService(db)

    return service.get_all()


@router.get(
    "/portfolio/{portfolio_id}",
    response_model=list[SocialLinkResponse],
)
def get_social_links_by_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
):
    service = SocialLinkService(db)

    try:
        return service.get_by_portfolio_id(portfolio_id)

    except PortfolioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{social_link_id}",
    response_model=SocialLinkResponse,
)
def get_social_link(
    social_link_id: int,
    db: Session = Depends(get_db),
):
    service = SocialLinkService(db)

    try:
        return service.get_by_id(social_link_id)

    except SocialLinkNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{social_link_id}",
    response_model=SocialLinkResponse,
)
def update_social_link(
    social_link_id: int,
    data: SocialLinkUpdate,
    db: Session = Depends(get_db),
):
    service = SocialLinkService(db)

    try:
        return service.update(social_link_id, data)

    except SocialLinkNotFoundError as exc:
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
    "/{social_link_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_social_link(
    social_link_id: int,
    db: Session = Depends(get_db),
):
    service = SocialLinkService(db)

    try:
        service.delete(social_link_id)

    except SocialLinkNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
