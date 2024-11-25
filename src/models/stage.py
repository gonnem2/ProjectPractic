from sqlalchemy import Column, ForeignKey, Integer, String, DateTime

from sqlalchemy.orm import relationship

from src.core.db import Base


class Stage(Base):
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True, index=True)
    rezume_id = Column(Integer, ForeignKey("rezumes.id"))
    name = Column(String, nullable=False)
    start = Column(DateTime)
    end = Column(DateTime)

    rezume = relationship("Rezume", back_populates="stage")
    sla_setting = relationship("SLASettings", back_populates="stage")
