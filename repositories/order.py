from PyQt6.QtCore import QDate
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from repositories.base import BaseRepository, ABC
from consts import *


class OrderModel:
    def __init__(self,
                 id=0,
                 price='0',
                 deadline=QDate.currentDate(),
                 client_id=0,
                 creation_date=QDate.currentDate(),
                 done=False):
        self.id = id
        self.price = price
        self.deadline = deadline
        self.client_id = client_id
        self.creation_date = creation_date
        self.done = done


class OrderOverallInfoModel:
    def __init__(self, fullname, price, deadline, creation_date, done):
        self.fullname = fullname
        self.price = price
        self.deadline = deadline
        self.creation_date = creation_date
        self.done = done


class FinishedOrderInfoModel:
    def __init__(self, id, client_name, price, deadline, creation_date):
        self.id = id
        self.client_name = client_name
        self.price = price
        self.deadline = deadline
        self.creation_date = creation_date

class UnfinishedOrderInfoModel:
    def __init__(self, id, price, deadline, client_name, creation_date, program_name, repo, stack, dev_group_name):
        self.id = id
        self.price = price
        self.deadline = deadline
        self.client_name = client_name
        self.creation_date = creation_date
        self.program_name = program_name
        self.repo = repo
        self.stack = stack
        self.dev_group_name = dev_group_name


class OrderRepository(BaseRepository, ABC):
    pass


class OrderRepositoryImpl(OrderRepository):

    def get_all(self) -> list[OrderModel]:
        query_text = 'SELECT * FROM orders ORDER BY id'
        query = QSqlQuery(self.db)
        query.prepare(query_text)

        if not query.exec():
            exit("Couldn't execute the query!" + self.db.lastError().databaseText())

        res = []
        while query.next():
            res.append(OrderModel(query.value(0),
                                  query.value(1),
                                  query.value(2),
                                  query.value(3),
                                  query.value(4),
                                  query.value(5)))

        return res

    def get_orders_by_client_id(self, user_id) -> list[OrderModel] | None:
        query_text = 'SELECT * FROM orders WHERE client_id=?'
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(user_id)

        if not query.exec():
            print('E: Could not execute the query!')
            return None

        res = []
        while query.next():
            res.append(OrderModel(query.value(0),
                                  query.value(1),
                                  query.value(2),
                                  query.value(3),
                                  query.value(4),
                                  query.value(5)))

        return res

    def delete(self, id):
        query_text = 'DELETE FROM orders WHERE id=?'
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(id)

        return query.exec()

    def update(self, data: OrderModel):
        query_text = "UPDATE orders SET price=?, deadline=?, client_id=?, creation_date=?, done=? WHERE id=?"

        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(data.price)
        query.addBindValue(data.deadline)
        query.addBindValue(data.client_id)
        query.addBindValue(data.creation_date)
        query.addBindValue(data.done)
        query.addBindValue(data.id)

        return query.exec()

    def create(self, data: OrderModel):
        query_text = ('INSERT INTO orders (price, deadline, client_id, creation_date, done) '
                      'VALUES (?, ?, ?, ?, ?)')
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(data.price)
        query.addBindValue(data.deadline)
        query.addBindValue(data.client_id)
        query.addBindValue(data.creation_date)
        query.addBindValue(data.done)

        return query.exec()

    def get_orders_overall_info(self) -> list[OrderOverallInfoModel]:
        query_text = 'SELECT clients.fullname, orders.price, orders.deadline, orders.creation_date, orders.done from Orders JOIN clients ON clients.id=orders.client_id'
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.exec()

        res = []
        while query.next():
            res.append(OrderOverallInfoModel(query.value(0),
                                             query.value(1),
                                             query.value(2),
                                             query.value(3),
                                             query.value(4)))
        return res

    def get_unfinished_orders(self) -> list[FinishedOrderInfoModel]:
        query_text = 'SELECT orders.id, orders.price, orders.deadline, clients.fullname, orders.creation_date, programs.name, programs.repo, programs.tech_stack, dev_groups.name from orders JOIN clients on clients.id=orders.client_id JOIN programs on programs.order_id=orders.id JOIN dev_groups on dev_groups.id=programs.dev_group_id'
        query = QSqlQuery(self.db)
        query.prepare(query_text)

        if not query.exec():
            return None

        res = []
        while query.next():
            res.append(UnfinishedOrderInfoModel(query.value(0),
                                                query.value(1),
                                                query.value(2),
                                                query.value(3),
                                                query.value(4),
                                                query.value(5),
                                                query.value(6),
                                                query.value(7),
                                                query.value(8)))
        return res
    
    def get_finished_orders(self) -> list[UnfinishedOrderInfoModel]:
        query_text = 'SELECT orders.id, clients.fullname, orders.price, orders.deadline, orders.creation_date from Orders JOIN clients ON clients.id=orders.client_id'
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.exec()

        res = []
        while query.next():
            res.append(FinishedOrderInfoModel(query.value(0),
                                              query.value(1),
                                              query.value(2),
                                              query.value(3),
                                              query.value(4)))
        return res


order_repo_impl = OrderRepositoryImpl()
