from sqlalchemy import Column, Integer, ForeignKey, DateTime, BIGINT

from sqlalchemy.orm import relationship

from app.core.db import Base


class SLASettings(Base):
    __tablename__ = "sla_settings"

    id = Column(Integer, primary_key=True, index=True)
    stage_id = Column(Integer, ForeignKey("stages.id"))
    max_time = Column(Integer)

    stage = relationship("Stage", back_populates="sla_setting")
