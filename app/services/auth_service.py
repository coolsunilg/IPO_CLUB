from sqlalchemy.orm import Session

from app.models.user import Member


class MemberService:

    @staticmethod
    def get_all(db: Session):
        return (
            db.query(Member)
            .filter(Member.is_active == True)
            .order_by(Member.id.desc())
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, member_id: int):
        return (
            db.query(Member)
            .filter(
                Member.id == member_id,
                Member.is_active == True
            )
            .first()
        )

    @staticmethod
    def get_by_client_id(db: Session, client_id: str):
        return (
            db.query(Member)
            .filter(Member.client_id == client_id)
            .first()
        )

    @staticmethod
    def add(db: Session, member: Member):

        db.add(member)

        db.commit()

        db.refresh(member)

        return member

    @staticmethod
    def save(db: Session):

        db.commit()

    @staticmethod
    def delete(db: Session, member: Member):

        member.is_active = False

        db.commit()