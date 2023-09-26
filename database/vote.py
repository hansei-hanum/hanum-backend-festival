from .core import Base

from sqlalchemy import BOOLEAN, Column
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT, DATETIME, ENUM
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql import func


class VoteField(Base):
    __tablename__ = "VoteFields"
    __table_args__ = {"mysql_charset": "utf8mb4"}

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    value = Column(VARCHAR(255), nullable=False)
    vote_table_id = Column(
        BIGINT(unsigned=True),
        ForeignKey("VoteTables.id", ondelete="CASCADE"),
        nullable=False,
    )
    vote_table = relationship("VoteTable", foreign_keys="VoteField.vote_table_id")
    created_at = Column(DATETIME, nullable=False, server_default=func.now())


class Vote(Base):
    __tablename__ = "Votes"
    __table_args__ = {"mysql_charset": "utf8mb4"}

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    user_id = Column(
        BIGINT(unsigned=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    vote_table_id = Column(
        BIGINT(unsigned=True),
        ForeignKey("VoteTables.id", ondelete="CASCADE"),
        nullable=False,
    )
    vote_table = relationship("VoteTable", foreign_keys="Vote.vote_table_id")
    vote_field_id = Column(
        BIGINT(unsigned=True),
        ForeignKey("VoteFields.id", ondelete="CASCADE"),
        nullable=False,
    )
    vote_field = relationship("VoteField", foreign_keys="Vote.vote_field_id")
    created_at = Column(DATETIME, nullable=False, server_default=func.now())


class VoteTable(Base):
    __tablename__ = "VoteTables"
    __table_args__ = {"mysql_charset": "utf8mb4"}

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    active = Column(BOOLEAN, nullable=False, server_default="0")
    start_at = Column(DATETIME, nullable=False, server_default=func.now())
    end_at = Column(DATETIME, nullable=False, server_default=func.now())
    title = Column(VARCHAR(255), nullable=False)
    created_at = Column(DATETIME, nullable=False, server_default=func.now())
    updated_at = Column(DATETIME, nullable=False, server_default=func.now(), onupdate=func.now())

    fields = relationship("VoteField", foreign_keys="VoteField.vote_table_id")
    votes = relationship("Vote", foreign_keys="Vote.vote_table_id")
