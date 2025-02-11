from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Enum,
    DateTime,
    Table as SQLTable,
    create_engine,
)
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy.types import Date

Base = declarative_base()


class Reservation(Base):
    __tablename__ = "reservation"

    id = Column(Integer, primary_key=True)
    arriving_at = Column(DateTime, nullable=True)
    client_name = Column(String, nullable=False)
    client_phone = Column(String, nullable=False)
    number_of_people = Column(Integer, nullable=False)


DATABASE_URL = "sqlite:///data.db"

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

print("\nBase de datos creada con éxito / Database created successfully")
