from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.certification import Certification


class CertificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, certification: Certification) -> Certification:
        self.db.add(certification)
        self.db.commit()
        self.db.refresh(certification)
        return certification

    def get_all(self) -> list[Certification]:
        statement = select(Certification).order_by(
            Certification.position,
            Certification.id,
        )
        return list(self.db.scalars(statement).all())

    def get_by_id(
        self,
        certification_id: int,
    ) -> Certification | None:
        statement = select(Certification).where(
            Certification.id == certification_id
        )
        return self.db.scalar(statement)

    def get_by_portfolio_id(
        self,
        portfolio_id: int,
    ) -> list[Certification]:
        statement = (
            select(Certification)
            .where(Certification.portfolio_id == portfolio_id)
            .order_by(
                Certification.position,
                Certification.id,
            )
        )
        return list(self.db.scalars(statement).all())

    def update(
        self,
        certification: Certification,
    ) -> Certification:
        self.db.commit()
        self.db.refresh(certification)
        return certification

    def delete(self, certification: Certification) -> None:
        self.db.delete(certification)
        self.db.commit()
