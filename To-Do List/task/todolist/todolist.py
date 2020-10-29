# Import necessary modules
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

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
	print("""\n1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")


def show_todays_tasks():
	today = datetime.today()
	print(f"\nToday {today.strftime('%d %b')}:")
	tasks = session.query(Table).filter(Table.deadline == today.date()).all()
	if tasks:
		for index, task in enumerate(tasks):
			print(f"{index + 1}. {task.task}")
	else:
		print("Nothing to do!")


def show_this_weeks_tasks():
	today = datetime.today()
	for day in range(7):
		date = today.date() + timedelta(day)
		tasks = session.query(Table).filter(Table.deadline == date).all()
		print(f"\n{date.strftime('%A %-d %b')}:")
		if tasks:
			for index, task in enumerate(tasks):
				print(f"{index + 1}. {task.task}")
		else:
			print("Nothing to do!")


def show_all_tasks():
	tasks = session.query(Table).order_by(Table.deadline).all()
	if tasks:
		print()
		for index, task in enumerate(tasks):
			print(f"{index + 1}. {task.task}. {task.deadline.strftime('%-d %b')}")
	else:
		print("\nNothing to do!")


def show_missed_tasks():
	missed_tasks = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
	print("\nMissed tasks:")
	if missed_tasks:
		for index, task in enumerate(missed_tasks):
			print(f"{index + 1}. {task.task}. {task.deadline.strftime('%-d %b')}")
	else:
		print("Nothing is missed!")


def add_task():
	new_task = input("\nEnter task")
	new_deadline = datetime.strptime(input("Enter deadline"), "%Y-%m-%d").date()
	new_row = Table(task=new_task, deadline=new_deadline)
	session.add(new_row)
	session.commit()
	print("The task has been added!")


def delete_task():
	index_to_delete = int(input(f"Choose the number of the task you want to delete: \n {show_all_tasks()} \n"))
	session.delete(session.query(Table).all()[index_to_delete - 1])
	session.commit()
	print("The task has been deleted!")


def main():
	while True:
		show_menu()
		user_choice = input()
		if user_choice == "1":
			show_todays_tasks()
		elif user_choice == "2":
			show_this_weeks_tasks()
		elif user_choice == "3":
			show_all_tasks()
		elif user_choice == "4":
			show_missed_tasks()
		elif user_choice == "5":
			add_task()
		elif user_choice == "6":
			delete_task()
		elif user_choice == "0":
			print("\nBye!")
			break


main()
