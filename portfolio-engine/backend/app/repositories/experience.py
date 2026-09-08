from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.experience import Experience


class ExperienceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, experience: Experience) -> Experience:
        self.db.add(experience)
        self.db.commit()
        self.db.refresh(experience)
        return experience

    def get_all(self) -> list[Experience]:
        statement = (
            select(Experience)
            .order_by(Experience.position, Experience.id)
        )
        return list(self.db.scalars(statement).all())

    def get_by_id(self, experience_id: int) -> Experience | None:
        statement = select(Experience).where(
            Experience.id == experience_id
        )
        return self.db.scalar(statement)

    def get_by_portfolio_id(
        self,
        portfolio_id: int,
    ) -> list[Experience]:
        statement = (
            select(Experience)
            .where(Experience.portfolio_id == portfolio_id)
            .order_by(Experience.position, Experience.id)
        )
        return list(self.db.scalars(statement).all())

    def update(self, experience: Experience) -> Experience:
        self.db.commit()
        self.db.refresh(experience)
        return experience

    def delete(self, experience: Experience) -> None:
        self.db.delete(experience)
        self.db.commit()
