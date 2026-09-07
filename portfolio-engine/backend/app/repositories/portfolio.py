from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.portfolio import Portfolio


class PortfolioRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, portfolio: Portfolio) -> Portfolio:
        self.db.add(portfolio)
        self.db.commit()
        self.db.refresh(portfolio)
        return portfolio

    def get_all(self) -> list[Portfolio]:
        statement = select(Portfolio).order_by(Portfolio.id)
        return list(self.db.scalars(statement).all())

    def get_by_id(self, portfolio_id: int) -> Portfolio | None:
        statement = select(Portfolio).where(Portfolio.id == portfolio_id)
        return self.db.scalar(statement)

    def get_by_slug(self, slug: str) -> Portfolio | None:
        statement = select(Portfolio).where(Portfolio.slug == slug)
        return self.db.scalar(statement)

    def update(self, portfolio: Portfolio) -> Portfolio:
        self.db.commit()
        self.db.refresh(portfolio)
        return portfolio

    def delete(self, portfolio: Portfolio) -> None:
        self.db.delete(portfolio)
        self.db.commit()
