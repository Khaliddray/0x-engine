from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.education import Education


class EducationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, education: Education) -> Education:
        self.db.add(education)
        self.db.commit()
        self.db.refresh(education)
        return education

    def get_all(self) -> list[Education]:
        statement = select(Education).order_by(
            Education.position,
            Education.id,
        )
        return list(self.db.scalars(statement).all())

    def get_by_id(self, education_id: int) -> Education | None:
        statement = select(Education).where(
            Education.id == education_id
        )
        return self.db.scalar(statement)

    def get_by_portfolio_id(
        self,
        portfolio_id: int,
    ) -> list[Education]:
        statement = (
            select(Education)
            .where(Education.portfolio_id == portfolio_id)
            .order_by(
                Education.position,
                Education.id,
            )
        )
        return list(self.db.scalars(statement).all())

    def update(self, education: Education) -> Education:
        self.db.commit()
        self.db.refresh(education)
        return education

    def delete(self, education: Education) -> None:
        self.db.delete(education)
        self.db.commit()
