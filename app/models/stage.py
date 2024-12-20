from sqlalchemy import Column, ForeignKey, Integer, String, DateTime

from sqlalchemy.orm import relationship

from app.core.db import Base


class Stage(Base):
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    rezume = relationship("Rezume", back_populates="stage")
    sla_setting = relationship("SLASettings", back_populates="stage")
