from .core import Base

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT, DATETIME, ENUM
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql import func


class LuckyToken(Base):
    __tablename__ = "luckytokens"
    __table_args__ = {"mysql_charset": "utf8mb4"}

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    user_id = Column(
        BIGINT(unsigned=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
    )
    user = relationship("User", foreign_keys="LuckyToken.user_id")
    token = Column(VARCHAR(255), nullable=False)
    created_at = Column(DATETIME, server_default=func.now())
    used_at = Column(DATETIME, server_default=func.now(), onupdate=func.now())


class LuckyNumber(Base):
    __tablename__ = "luckynumbers"
    __table_args__ = {"mysql_charset": "utf8mb4"}

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    user_id = Column(
        BIGINT(unsigned=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    user = relationship("User", foreign_keys="LuckyNumber.user_id")
    created_at = Column(DATETIME, server_default=func.now())
