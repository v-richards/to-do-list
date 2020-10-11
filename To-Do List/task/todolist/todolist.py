# Import necessary modules
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime


# Connect to the database
engine = create_engine("sqlite:///todo.db?check_same_thread=False")

Base = declarative_base()


# Create the model class
class Table(Base):

    """Table class that creates rows in the database"""

    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String, default="default_value")
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


# Create a table in the database
Base.metadata.create_all(engine)

# Create a session to access the database
Session = sessionmaker(bind=engine)
session = Session()

# # Create a row in the table and commit it to the database
# new_row = Table(string_field="This is string field!", date_field=datetime.strptime("01-24-2020", "%m-%d-%y").date())
# session.add(new_row)
# session.commit()

# Get all rows from the table using the query() method (returns a list)
rows = session.query(Table).all()

# first_row = rows[0]  # If rows isn't empty
# print(first_row.id)
# print(first_row.string_field)
# print(first_row)


def show_menu():
    print("1) Today's tasks\n"
          "2) Add task\n"
          "0) Exit")


def show_tasks():
    tasks = session.query(Table).all()
    if tasks:
        print("\nToday:")
        for task in tasks:
            print(task)
        print("")
    else:
        print("\nNothing to do!")


def add_task():
    user_input = input("\nEnter task\n")
    new_task = Table(task=user_input)
    session.add(new_task)
    session.commit()
    print("The task has been added!\n")


def main():
    while True:
        show_menu()
        user_choice = input()
        if user_choice == "1":
            show_tasks()
        elif user_choice == "2":
            add_task()
        elif user_choice == "0":
            print("\nBye!")
            break


main()
