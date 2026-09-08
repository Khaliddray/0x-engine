from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.skill import Skill


class SkillRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, skill: Skill) -> Skill:
        self.db.add(skill)
        self.db.commit()
        self.db.refresh(skill)
        return skill

    def get_all(self) -> list[Skill]:
        statement = (
            select(Skill)
            .order_by(Skill.position, Skill.id)
        )
        return list(self.db.scalars(statement).all())

    def get_by_id(self, skill_id: int) -> Skill | None:
        statement = select(Skill).where(Skill.id == skill_id)
        return self.db.scalar(statement)

    def get_by_slug(self, slug: str) -> Skill | None:
        statement = select(Skill).where(Skill.slug == slug)
        return self.db.scalar(statement)

    def get_by_portfolio_id(
        self,
        portfolio_id: int,
    ) -> list[Skill]:
        statement = (
            select(Skill)
            .where(Skill.portfolio_id == portfolio_id)
            .order_by(Skill.position, Skill.id)
        )
        return list(self.db.scalars(statement).all())

    def update(self, skill: Skill) -> Skill:
        self.db.commit()
        self.db.refresh(skill)
        return skill

    def delete(self, skill: Skill) -> None:
        self.db.delete(skill)
        self.db.commit()
