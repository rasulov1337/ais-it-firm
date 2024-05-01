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


order_repo_impl = OrderRepositoryImpl()
