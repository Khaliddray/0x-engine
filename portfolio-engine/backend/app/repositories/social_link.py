from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.social_link import SocialLink


class SocialLinkRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, social_link: SocialLink) -> SocialLink:
        self.db.add(social_link)
        self.db.commit()
        self.db.refresh(social_link)
        return social_link

    def get_all(self) -> list[SocialLink]:
        statement = select(SocialLink).order_by(
            SocialLink.position,
            SocialLink.id,
        )
        return list(self.db.scalars(statement).all())

    def get_by_id(
        self,
        social_link_id: int,
    ) -> SocialLink | None:
        statement = select(SocialLink).where(
            SocialLink.id == social_link_id
        )
        return self.db.scalar(statement)

    def get_by_portfolio_id(
        self,
        portfolio_id: int,
    ) -> list[SocialLink]:
        statement = (
            select(SocialLink)
            .where(SocialLink.portfolio_id == portfolio_id)
            .order_by(
                SocialLink.position,
                SocialLink.id,
            )
        )
        return list(self.db.scalars(statement).all())

    def update(
        self,
        social_link: SocialLink,
    ) -> SocialLink:
        self.db.commit()
        self.db.refresh(social_link)
        return social_link

    def delete(self, social_link: SocialLink) -> None:
        self.db.delete(social_link)
        self.db.commit()
