from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.resume import Resume


class ResumeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, resume: Resume) -> Resume:
        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)
        return resume

    def get_all(self) -> list[Resume]:
        statement = select(Resume).order_by(Resume.id)
        return list(self.db.scalars(statement).all())

    def get_by_id(
        self,
        resume_id: int,
    ) -> Resume | None:
        statement = select(Resume).where(
            Resume.id == resume_id
        )
        return self.db.scalar(statement)

    def get_by_portfolio_id(
        self,
        portfolio_id: int,
    ) -> list[Resume]:
        statement = (
            select(Resume)
            .where(Resume.portfolio_id == portfolio_id)
            .order_by(Resume.id)
        )
        return list(self.db.scalars(statement).all())

    def update(
        self,
        resume: Resume,
    ) -> Resume:
        self.db.commit()
        self.db.refresh(resume)
        return resume

    def delete(self, resume: Resume) -> None:
        self.db.delete(resume)
        self.db.commit()
