from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.public_portfolio import PublicPortfolioResponse
from app.services.public_portfolio import (
    PublicPortfolioNotFoundError,
    PublicPortfolioService,
)


router = APIRouter(
    prefix="/api/public/portfolios",
    tags=["Public Portfolio"],
)


@router.get(
    "/{slug}",
    response_model=PublicPortfolioResponse,
)
def get_public_portfolio(
    slug: str,
    db: Session = Depends(get_db),
):
    service = PublicPortfolioService(db)

    try:
        return service.get_by_slug(slug)
    except PublicPortfolioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
