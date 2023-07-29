from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from .controller import Base

class Voice(Base):
    """
    Voice model -> Elevenlabs
    """
    __tablename__ = "voices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    characters = relationship('Character', back_populates='voice')


class Character(Base):
    """
    Our Character model with the Elevenlabs mapping
    """
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    avatar_data = Column(LargeBinary)
    description = Column(String)
    labels = Column(String)
    rating = Column(Integer)
    voice_id = Column(Integer, ForeignKey('voices.id'))
    voice = relationship('Voice', back_populates='characters')
