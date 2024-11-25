from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String

from sqlalchemy.orm import relationship

from src.core.db import Base


class Rezume(Base):
    __tablename__ = "rezumes"

    id = Column(Integer, primary_key=True, index=True)
    vacancy_id = Column(Integer, ForeignKey("vacancies.id"))
    source = Column(String, nullable=True)
    text = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    uploadet_ad = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="rezume")
    vacancy = relationship("Vacancy", back_populates="rezume")
    violation = relationship("Violation", back_populates="rezume")
    stage = relationship("Stage", back_populates="rezume")
