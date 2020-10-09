from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

    def deadline_to_string(self):
        return str(self.deadline.strftime('%#d %b'))

    @staticmethod
    def list_all_tasks():
        for task in session.query(Table).order_by(Table.deadline):
            print(task.task, task.deadline)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def days_task(day):
    return session.query(Table).filter(Table.deadline == day).all()


while True:
    user_input = input('1) Today\'s tasks\n2) Week\'s tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete '
                       'task\n0) Exit\n')

    if user_input == '1':
        print('Today ' + str(datetime.today().strftime("%d %b")))
        rows = days_task(datetime.today().date())
        if not rows:
            print('Nothing to do!\n')
            continue
        for row in rows:
            print(row)

    elif user_input == '2':
        for day in range(7):
            print((datetime.today() + timedelta(day)).strftime('%A %d %b') + ':')
            rows = days_task(datetime.today().date() + timedelta(day))
            if not rows:
                print('Nothing to do!\n')
                continue
            for i, row in enumerate(rows):
                print(str(i + 1) + '. ' + str(row) + '\n')

    elif user_input == '3':
        print('All tasks:')
        rows = session.query(Table).filter(Table.deadline >= datetime.today().date()).order_by(Table.deadline).all()
        for i, row in enumerate(rows):
            print(str(i + 1) + '. ' + str(row) + '. ' + row.deadline_to_string())

    elif user_input == '4':
        print('Missed tasks:')
        rows = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
        if not rows:
            print('Nothing is missed!')
            continue
        for i, row in enumerate(rows):
            print(str(i + 1) + '. ' + str(row) + '. ' + row.deadline_to_string())
        print()

    elif user_input == '5':
        task_name = input('Enter task\n')
        deadline = input('Enter deadline\n')
        new_row = Table(task=task_name,
                        deadline=datetime.strptime(deadline, '%Y-%m-%d').date())
        session.add(new_row)
        session.commit()
        print('The task has been added')

    elif user_input == '6':
        print('Choose the number of the task you want to delete:')
        rows = session.query(Table).order_by(Table.deadline).all()
        for i, row in enumerate(rows):
            print(str(i + 1) + '. ' + str(row) + '. ' + row.deadline_to_string())
        deletion_n = int(input())
        session.delete(rows[deletion_n - 1])
        session.commit()

    elif user_input == '0':
        print('Bye!')
        exit()
