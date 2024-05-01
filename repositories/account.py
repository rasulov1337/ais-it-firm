from repositories.base import BaseRepository, ABC, abstractmethod

from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from consts import *


class AccountModel:
    class Type:
        ADMIN = 'admin'
        USER = 'user'

    def __init__(self, id=0, client_id=0, login='', password='', type=Type.USER):
        self.id = id
        self.client_id = client_id
        self.login = login
        self.password = password
        self.type = type


class AccountRepository(BaseRepository, ABC):
    @abstractmethod
    def get(self, login, password) -> AccountModel:
        pass


class AccountRepositoryImpl(AccountRepository):
    def create(self, data):
        query_text = 'INSERT INTO accounts (client_id, login, password, type) VALUES (?, ?, ?, ?)'
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(data.client_id)
        query.addBindValue(data.login)
        query.addBindValue(data.password)
        query.addBindValue(data.type)

        return query.exec()

    def get(self, login: str, password: str) -> AccountModel:
        query_text = 'SELECT * FROM accounts WHERE login=? AND password=?'
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(login)
        query.addBindValue(password)

        if not query.exec():
            print("E: Couldn't execute the query!", self.db.lastError().databaseText())
            return None

        query.next()
        if query.value(0) is None:
            return None

        return AccountModel(query.value(0),
                            query.value(1),
                            query.value(2),
                            query.value(3),
                            query.value(4))

    def get_all(self):
        query_text = 'SELECT * FROM accounts ORDER BY id'
        query = QSqlQuery(self.db)
        query.prepare(query_text)

        if not query.exec():
            exit("Couldn't execute the query!" + self.db.lastError().databaseText())

        res = []
        while query.next():
            res.append(AccountModel(query.value(0),
                                    query.value(1),
                                    query.value(2),
                                    query.value(3),
                                    query.value(4)))

        return res

    def delete(self, id: int) -> bool:
        query_text = 'DELETE FROM accounts WHERE id=?'
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(id)

        return query.exec()

    def update(self, data) -> bool:
        query_text = "UPDATE accounts SET client_id=?, login=?, password=?, type=? WHERE id=?"

        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(data.client_id)
        query.addBindValue(data.login)
        query.addBindValue(data.password)
        query.addBindValue(data.type)
        query.addBindValue(data.id)

        return query.exec()


account_repo_impl = AccountRepositoryImpl()
