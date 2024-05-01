from abc import ABC, abstractmethod

from PyQt6.QtCore import QDate
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from consts import *


class Employee:
    def __init__(self,
                 id_=0,
                 fullname='',
                 birth_date=QDate.currentDate(),
                 hire_date=QDate.currentDate(),
                 salary='0',
                 dev_group_id=0):
        self.id = id_
        self.fullname = fullname
        self.birth_date = birth_date
        self.hire_date = hire_date
        self.salary = salary
        self.dev_group_id = dev_group_id


class EmployeeRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Employee]:
        pass

    @abstractmethod
    def delete(self, id: int):
        pass

    @abstractmethod
    def update(self, data: Employee):
        pass

    @abstractmethod
    def create(self, data: Employee):
        pass

    @abstractmethod
    def find_by_name(self, fullname: str) -> list[Employee]:
        pass


class EmployeeRepositoryImpl(EmployeeRepository):
    def __init__(self):
        # Init DB connection
        self.db = QSqlDatabase.addDatabase('QPSQL')
        self.db.setHostName(DB_HOST_NAME)
        self.db.setPort(DB_PORT)
        self.db.setDatabaseName(DB_NAME)
        self.db.setUserName(DB_USERNAME)
        self.db.setPassword(DB_PASSWORD)

        self.db.open()
        if not self.db.open():
            print('Unable to connect to the database: ', self.db.lastError().databaseText())
            exit(-1)

    def get_all(self):
        query_text = 'SELECT * FROM employees ORDER BY id'
        query = QSqlQuery(self.db)
        query.prepare(query_text)

        if not query.exec():
            exit("Couldn't execute the query!" + self.db.lastError().databaseText())

        res = []
        while query.next():
            res.append(Employee(query.value(0),
                                query.value(1),
                                query.value(2),
                                query.value(4),
                                query.value(3),
                                query.value(5)))

        return res

    def delete(self, id):
        query_text = 'DELETE FROM employees WHERE id=?'
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(id)

        return query.exec()

    def update(self, data: Employee):
        query_text = "UPDATE employees SET fullname=?, birth_date=?, salary=?, hire_date=?, dev_group_id=? WHERE id=?"

        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(data.fullname)
        query.addBindValue(data.birth_date)
        query.addBindValue(data.salary)
        query.addBindValue(data.hire_date)
        query.addBindValue(data.dev_group_id)
        query.addBindValue(data.id)

        return query.exec()

    def create(self, data: Employee):
        query_text = ('INSERT INTO employees (fullname, birth_date, salary, hire_date, dev_group_id) '
                      'VALUES (?, ?, ?, ?, ?)')
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(data.fullname)
        query.addBindValue(data.birth_date)
        query.addBindValue(data.salary)
        query.addBindValue(data.hire_date)
        query.addBindValue(data.dev_group_id)

        print(query.lastQuery())

        return query.exec()

    def find_by_name(self, fullname: str) -> list[Employee]:
        query_text = 'SELECT * FROM employees WHERE fullname LIKE ?'
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(fullname + '%')

        if not query.exec():
            print("Couldn't execute the query!")
            return []

        res = []

        while query.next():
            res.append(Employee(query.value(0),
                                query.value(1),
                                query.value(2),
                                query.value(4),
                                query.value(3),
                                query.value(5)))

        return res

    def get_employees_by_dev_group_id(self, dev_group_id: int) -> list[Employee]:
        query_text = 'SELECT * FROM employees WHERE dev_group_id=?'
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(dev_group_id)

        if not query.exec():
            print("Couldn't execute the query!")
            return []

        res = []

        while query.next():
            res.append(Employee(query.value(0),
                                query.value(1),
                                query.value(2),
                                query.value(4),
                                query.value(3),
                                query.value(5)))

        return res


employee_repo_impl = EmployeeRepositoryImpl()
