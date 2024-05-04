from abc import ABC

from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from consts import *

from repositories.base import BaseRepository


class DevGroupModel:
    def __init__(self, id_=0, name='', tech_stack=''):
        self.id = id_
        self.name = name
        self.tech_stack = tech_stack


class DevGroupRepository(BaseRepository, ABC):
    def get_all(self) -> DevGroupModel:
        pass


class DevGroupRepositoryImpl(DevGroupRepository):
    def get(self, id: int) -> DevGroupModel:
        query_text = 'SELECT * FROM dev_groups WHERE id=?'
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(id)

        if not query.exec():
            print("E: Couldn't execute the query!")
            return None

        query.next()

        return DevGroupModel(query.value(0),
                             query.value(1),
                             query.value(2))
    
    def get_name(self, id: int) -> str:
        query_text = 'SELECT dev_groups.name FROM dev_groups WHERE id=?'
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(id)

        if not query.exec():
            exit("Couldn't execute the query!")

        query.next()

        return query.value(0)

    def get_all(self):
        query_text = 'SELECT * FROM dev_groups ORDER BY id'
        query = QSqlQuery(self.db)
        query.prepare(query_text)

        if not query.exec():
            print("Couldn't execute the query!")
            return None

        res = []
        while query.next():
            res.append(DevGroupModel(query.value(0),
                                     query.value(1),
                                     query.value(2)))

        return res

    def delete(self, id: int):
        query_text = 'DELETE FROM dev_groups WHERE id=?'
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(id)

        return query.exec()

    def create(self, data):
        query_text = ('INSERT INTO dev_groups (name, tech_stack) '
                      'VALUES (?, ?)')
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(data.name)
        query.addBindValue(data.tech_stack)

        return query.exec()

    def update(self, data):
        query_text = "UPDATE dev_groups SET name=?, tech_stack=? WHERE id=?"

        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(data.name)
        query.addBindValue(data.tech_stack)
        query.addBindValue(data.id)

        return query.exec()


dev_group_repo_impl = DevGroupRepositoryImpl()
