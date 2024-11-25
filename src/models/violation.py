from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

from sqlalchemy.orm import relationship

from src.core.db import Base


class Violation(Base):
    __tablename__ = "violations"

    id = Column(Integer, primary_key=True, index=True)
    sla_id = Column(Integer, ForeignKey("sla_settings.id"))
    rezume_id = Column(Integer, ForeignKey("rezumes.id"))
    date = Column(DateTime)

    sla = relationship("SLASettings", back_populates="violation")
    rezume = relationship("Rezume", back_populates="violation")
