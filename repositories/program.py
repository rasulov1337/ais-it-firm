from PyQt6.QtSql import QSqlQuery

from repositories.base import BaseRepository, ABC
from repositories.order import OrderModel


class ProgramModel:
    def __init__(self,
                 id=0,
                 repo='',
                 name='',
                 tech_stack='',
                 order_id=0,
                 dev_group_id=0):
        self.id = id
        self.repo = repo
        self.name = name
        self.tech_stack = tech_stack
        self.order_id = order_id
        self.dev_group_id = dev_group_id


class ProgramRepository(BaseRepository, ABC):
    pass


class ProgramRepositoryImpl(ProgramRepository):
    def get_all(self) -> list[ProgramModel]:
        query_text = 'SELECT * FROM programs ORDER BY id'
        query = QSqlQuery(self.db)
        query.prepare(query_text)

        if not query.exec():
            exit("Couldn't execute the query!" + self.db.lastError().databaseText())

        res = []
        while query.next():
            res.append(ProgramModel(query.value(0),
                                    query.value(1),
                                    query.value(2),
                                    query.value(3),
                                    query.value(4),
                                    query.value(5)))

        return res

    def delete(self, id):
        query_text = 'DELETE FROM programs WHERE id=?'
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(id)

        return query.exec()

    def update(self, data: ProgramModel):
        query_text = "UPDATE programs SET repo=?, name=?, tech_stack=?, order_id=?, dev_group_id=? WHERE id=?"

        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(data.repo)
        query.addBindValue(data.name)
        query.addBindValue(data.tech_stack)
        query.addBindValue(data.order_id)
        query.addBindValue(data.dev_group_id)
        query.addBindValue(data.id)

        return query.exec()

    def create(self, data: ProgramModel):
        query_text = 'INSERT INTO programs (repo, name, tech_stack, order_id, dev_group_id) VALUES (?, ?, ?, ?, ?)'
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(data.repo)
        query.addBindValue(data.name)
        query.addBindValue(data.tech_stack)
        query.addBindValue(data.order_id)
        query.addBindValue(data.dev_group_id)

        return query.exec()

    def get_programs_by_order_id(self, order_id: int):
        query_text = 'SELECT * FROM programs WHERE order_id=? ORDER BY id'
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(order_id)

        if not query.exec():
            exit("Couldn't execute the query!" + self.db.lastError().databaseText())

        res = []
        while query.next():
            res.append(ProgramModel(query.value(0),
                                    query.value(1),
                                    query.value(2),
                                    query.value(3),
                                    query.value(4),
                                    query.value(5)))

        return res

    def get_programs_by_name(self, name: str):
        query_text = 'SELECT * FROM programs WHERE name LIKE ?'
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(name + '%')

        if not query.exec():
            print("Couldn't execute the query!")
            return []

        res = []
        while query.next():
            res.append(ProgramModel(query.value(0),
                                    query.value(1),
                                    query.value(2),
                                    query.value(3),
                                    query.value(4),
                                    query.value(5)))

        return res

    def get_programs_and_their_orders(self, client_id: int) -> list[ProgramModel, OrderModel, str]:
        query_text = 'SELECT programs.*, orders.*, dev_groups.name FROM programs JOIN orders ON orders.id = programs.order_id JOIN dev_groups ON dev_groups.id = programs.dev_group_id WHERE orders.client_id=? ORDER BY programs.id'
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(client_id)

        if not query.exec():
            print("Couldn't execute the query!")
            return []

        res = []
        while query.next():
            res.append([ProgramModel(query.value(0),
                                     query.value(1),
                                     query.value(2),
                                     query.value(3),
                                     query.value(4),
                                     query.value(5)),
                        OrderModel(query.value(6),
                                   query.value(7),
                                   query.value(8),
                                   query.value(9),
                                   query.value(10),
                                   query.value(11)),
                        query.value(12)])

        return res


program_repo_impl = ProgramRepositoryImpl()
