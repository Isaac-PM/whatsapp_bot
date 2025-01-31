# from sqlalchemy import (
#     Column,
#     Integer,
#     String,
#     Float,
#     ForeignKey,
#     Enum,
#     DateTime,
#     Table as SQLTable,
# )
# from sqlalchemy.orm import relationship, declarative_base
# from sqlalchemy.types import Date
# import enum

# Base = declarative_base()


# # Enum for food categories
# # Enumerador para categorías de comida
# class FoodCategory(enum.Enum):
#     starter = "starter"  # Entrada
#     main_course = "main_course"  # Plato fuerte
#     beverage = "beverage"  # Bebida
#     dessert = "dessert"  # Postre


# # Association table for many-to-many relationship between Table and Reservation
# table_reservation_association = SQLTable(
#     "table_reservation",
#     Base.metadata,
#     Column("table_id", Integer, ForeignKey("table.id"), primary_key=True),
#     Column("reservation_id", Integer, ForeignKey("reservation.id"), primary_key=True),
# )

# # Association table for many-to-many relationship between Reservation and Food (Order)
# reservation_food_association = SQLTable(
#     "reservation_food",
#     Base.metadata,
#     Column("reservation_id", Integer, ForeignKey("reservation.id"), primary_key=True),
#     Column("food_id", Integer, ForeignKey("food.id"), primary_key=True),
# )


# class Table(Base):
#     __tablename__ = "table"

#     id = Column(Integer, primary_key=True)
#     capacity = Column(Integer, nullable=False)

#     # Relationship with reservations
#     reservations = relationship(
#         "Reservation", secondary=table_reservation_association, back_populates="tables"
#     )


# class Reservation(Base):
#     __tablename__ = "reservation"

#     id = Column(Integer, primary_key=True)
#     starting_time = Column(DateTime, nullable=False)
#     ending_time = Column(DateTime, nullable=False)
#     client_name = Column(String, nullable=False)

#     # Relationship with tables
#     tables = relationship(
#         "Table", secondary=table_reservation_association, back_populates="reservations"
#     )

#     # Relationship with food (orders)
#     food_orders = relationship(
#         "Food", secondary=reservation_food_association, back_populates="reservations"
#     )


# class Food(Base):
#     __tablename__ = "food"

#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     description = Column(String)
#     price = Column(Float, nullable=False)
#     category = Column(Enum(FoodCategory), nullable=False)

#     # Relationship with reservations
#     reservations = relationship(
#         "Reservation",
#         secondary=reservation_food_association,
#         back_populates="food_orders",
#     )


# # class ExecutiveMenu(Base):
# #     __tablename__ = "executive_menu"

# #     id = Column(Integer, primary_key=True)
# #     starter_id = Column(Integer, ForeignKey("food.id"), nullable=False)
# #     main_course_id = Column(Integer, ForeignKey("food.id"), nullable=False)
# #     beverage_id = Column(Integer, ForeignKey("food.id"), nullable=False)
# #     dessert_id = Column(Integer, ForeignKey("food.id"), nullable=False)
# #     discount_percentage = Column(Float, nullable=False)
# #     day_of_week = Column(String, nullable=False)

# #     # Relationships with food
# #     starter = relationship("Food", foreign_keys=[starter_id])
# #     main_course = relationship("Food", foreign_keys=[main_course_id])
# #     beverage = relationship("Food", foreign_keys=[beverage_id])
# #     dessert = relationship("Food", foreign_keys=[dessert_id])

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# # Import your schema from the earlier code
# # from your_schema_file import Base, Table, Reservation, Food, ExecutiveMenu

# # Step 1: Define the SQLite database file
# DATABASE_URL = "sqlite:///local_database.db"  # SQLite file in the current directory

# # Step 2: Create the engine
# engine = create_engine(DATABASE_URL, echo=True)

# # Step 3: Create all tables in the database
# Base.metadata.create_all(engine)

# # Step 4: Configure the session
# Session = sessionmaker(bind=engine)
# session = Session()


# # Step 5: Add some example data (optional)
# def populate_example_data(session):
#     # Example Food items
#     food1 = Food(
#         name="Caesar Salad",
#         description="Classic Caesar Salad",
#         price=7.99,
#         category=FoodCategory.starter,
#     )
#     food2 = Food(
#         name="Steak",
#         description="Grilled sirloin steak",
#         price=20.99,
#         category=FoodCategory.main_course,
#     )
#     food3 = Food(
#         name="Coke",
#         description="Coca-Cola 12 oz",
#         price=2.49,
#         category=FoodCategory.beverage,
#     )
#     food4 = Food(
#         name="Chocolate Cake",
#         description="Rich chocolate dessert",
#         price=6.99,
#         category=FoodCategory.dessert,
#     )

#     # Example table
#     table1 = Table(capacity=4)
#     table2 = Table(capacity=6)

#     # Example reservation
#     reservation1 = Reservation(
#         starting_time="2025-01-24 12:00:00",
#         ending_time="2025-01-24 14:00:00",
#         client_name="John Doe",
#         tables=[table1, table2],  # Linked tables
#         food_orders=[food1, food2, food3],  # Linked food orders
#     )

#     # Add to session and commit
#     session.add_all([food1, food2, food3, food4, table1, table2, reservation1])
#     session.commit()


# # Uncomment to populate example data
# # populate_example_data(session)

# print("SQLite database setup complete.")
