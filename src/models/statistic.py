from sqlalchemy import Column, Integer, Float, JSON, ARRAY
from src.core.db import Base


class Statistic(Base):
    __tablename__ = "stats"
    id = Column(Integer, index=True, primary_key=True)
    avg_time = Column(ARRAY(Float), nullable=False)
    stage_distribution = Column(JSON, nullable=False)
    source_distribution = Column(JSON, nullable=False)
    avg_in_position = Column(JSON, nullable=False)
    sla_violation = Column(Integer, nullable=True)
