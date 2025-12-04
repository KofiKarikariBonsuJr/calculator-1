from sqlalchemy import Column, Integer, Float, String, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base, relationship
import enum
from app.database import Base

Base = declarative_base()

class CalculationType(str, enum.Enum):
    add = "add"
    subtract = "subtract"
    multiply = "multiply"
    divide = "divide"

class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    type = Column(Enum(CalculationType), nullable=False)
   
    result = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", backref="calculations")