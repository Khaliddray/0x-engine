from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.resume import (
    ResumeCreate,
    ResumeResponse,
    ResumeUpdate,
)
from app.services.resume import (
    PortfolioNotFoundError,
    ResumeNotFoundError,
    ResumeService,
)


router = APIRouter(
    prefix="/api/resumes",
    tags=["Resumes"],
)


@router.post(
    "",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_resume(
    data: ResumeCreate,
    db: Session = Depends(get_db),
):
    service = ResumeService(db)

    try:
        return service.create(data)

    except PortfolioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[ResumeResponse],
)
def get_resumes(
    db: Session = Depends(get_db),
):
    service = ResumeService(db)

    return service.get_all()


@router.get(
    "/portfolio/{portfolio_id}",
    response_model=list[ResumeResponse],
)
def get_resumes_by_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
):
    service = ResumeService(db)

    try:
        return service.get_by_portfolio_id(portfolio_id)

    except PortfolioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{resume_id}",
    response_model=ResumeResponse,
)
def get_resume(
    resume_id: int,
    db: Session = Depends(get_db),
):
    service = ResumeService(db)

    try:
        return service.get_by_id(resume_id)

    except ResumeNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{resume_id}",
    response_model=ResumeResponse,
)
def update_resume(
    resume_id: int,
    data: ResumeUpdate,
    db: Session = Depends(get_db),
):
    service = ResumeService(db)

    try:
        return service.update(resume_id, data)

    except ResumeNotFoundError as exc:
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
    "/{resume_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_resume(
    resume_id: int,
    db: Session = Depends(get_db),
):
    service = ResumeService(db)

    try:
        service.delete(resume_id)

    except ResumeNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
