from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.skill import (
    SkillCreate,
    SkillResponse,
    SkillUpdate,
)
from app.services.skill import (
    PortfolioNotFoundError,
    SkillNotFoundError,
    SkillService,
    SkillSlugExistsError,
)


router = APIRouter(
    prefix="/api/skills",
    tags=["Skills"],
)


@router.post(
    "",
    response_model=SkillResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_skill(
    data: SkillCreate,
    db: Session = Depends(get_db),
):
    service = SkillService(db)

    try:
        return service.create(data)
    except PortfolioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except SkillSlugExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[SkillResponse],
)
def get_skills(
    db: Session = Depends(get_db),
):
    service = SkillService(db)
    return service.get_all()


@router.get(
    "/portfolio/{portfolio_id}",
    response_model=list[SkillResponse],
)
def get_skills_by_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
):
    service = SkillService(db)

    try:
        return service.get_by_portfolio_id(portfolio_id)
    except PortfolioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{skill_id}",
    response_model=SkillResponse,
)
def get_skill(
    skill_id: int,
    db: Session = Depends(get_db),
):
    service = SkillService(db)

    try:
        return service.get_by_id(skill_id)
    except SkillNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{skill_id}",
    response_model=SkillResponse,
)
def update_skill(
    skill_id: int,
    data: SkillUpdate,
    db: Session = Depends(get_db),
):
    service = SkillService(db)

    try:
        return service.update(skill_id, data)
    except SkillNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except PortfolioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except SkillSlugExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{skill_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
):
    service = SkillService(db)

    try:
        service.delete(skill_id)
    except SkillNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
