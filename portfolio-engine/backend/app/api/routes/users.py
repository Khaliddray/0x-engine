from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_superuser, get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.services.user import (
    UserAlreadyExistsError,
    UserNotFoundError,
    UserService,
)

router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
)


@router.get(
    "",
    response_model=list[UserResponse],
    dependencies=[Depends(get_current_superuser)],
)
def get_users(
    db: Session = Depends(get_db),
):
    service = UserService(db)
    return service.get_all()


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(get_current_user)],
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    service = UserService(db)
    try:
        return service.get_by_id(user_id)
    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(get_current_user)],
)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Only superusers can update other users; standard users can only update themselves
    if not current_user.is_superuser and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this user",
        )

    # Standard users cannot elevate privileges
    if not current_user.is_superuser:
        data.is_superuser = None

    service = UserService(db)
    try:
        return service.update(user_id, data)
    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except UserAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_superuser)],
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    service = UserService(db)
    try:
        service.delete(user_id)
    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
