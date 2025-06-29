from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class Clan(Base):
    __tablename__ = "clans"
    __table_args__ = {"schema": "api"}

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    name = Column(String, nullable=False)
    region = Column(String(4))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
