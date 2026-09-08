from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.portfolio_section import PortfolioSection


class PortfolioSectionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, section: PortfolioSection) -> PortfolioSection:
        self.db.add(section)
        self.db.commit()
        self.db.refresh(section)
        return section

    def get_all(self) -> list[PortfolioSection]:
        statement = (
            select(PortfolioSection)
            .order_by(PortfolioSection.position, PortfolioSection.id)
        )
        return list(self.db.scalars(statement).all())

    def get_by_id(self, section_id: int) -> PortfolioSection | None:
        statement = select(PortfolioSection).where(
            PortfolioSection.id == section_id
        )
        return self.db.scalar(statement)

    def get_by_slug(self, slug: str) -> PortfolioSection | None:
        statement = select(PortfolioSection).where(
            PortfolioSection.slug == slug
        )
        return self.db.scalar(statement)

    def get_by_portfolio_id(
        self,
        portfolio_id: int,
    ) -> list[PortfolioSection]:
        statement = (
            select(PortfolioSection)
            .where(PortfolioSection.portfolio_id == portfolio_id)
            .order_by(PortfolioSection.position, PortfolioSection.id)
        )
        return list(self.db.scalars(statement).all())

    def update(self, section: PortfolioSection) -> PortfolioSection:
        self.db.commit()
        self.db.refresh(section)
        return section

    def delete(self, section: PortfolioSection) -> None:
        self.db.delete(section)
        self.db.commit()
