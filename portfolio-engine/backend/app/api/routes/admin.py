from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.schemas.admin import AdminOverviewResponse
from app.services.admin import AdminService

router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    "/overview",
    response_model=AdminOverviewResponse,
)
def get_admin_overview(
    db: Session = Depends(get_db),
):
    service = AdminService(db)
    return service.get_overview()
