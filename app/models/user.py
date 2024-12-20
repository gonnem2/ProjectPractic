from sqlalchemy import Column, Integer, String, Boolean

from sqlalchemy.orm import relationship

from app.core import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_hr = Column(Boolean, default=True)
    is_team_lead = Column(Boolean, default=False)

    vacancy = relationship("Vacancy", back_populates="user")
    rezume = relationship("Rezume", back_populates="user")
