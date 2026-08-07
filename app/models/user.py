from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.core.database import Base


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)

    member_name = Column(String(100), nullable=False)

    client_id = Column(String(50), unique=True, nullable=False, index=True)

    password = Column(String(500), nullable=False)

    api_key = Column(String(500), nullable=False)

    totp_secret = Column(String(500), nullable=False)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )