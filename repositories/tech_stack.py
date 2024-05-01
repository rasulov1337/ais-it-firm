from PyQt6.QtSql import QSqlQuery

from repositories.base import BaseRepository, ABC


class TechStackModel:
    def __init__(self,
                 id=0,
                 tech_stack=''):
        self.id = id
        self.tech_stack = tech_stack


class TechStackRepository(BaseRepository, ABC):
    pass


class TechStackRepositoryImpl(TechStackRepository):
    def get_all(self) -> list[TechStackModel]:
        query_text = 'SELECT * FROM tech_stacks ORDER BY id'
        query = QSqlQuery(self.db)
        query.prepare(query_text)

        if not query.exec():
            exit("Couldn't execute the query!" + self.db.lastError().databaseText())

        res = []
        while query.next():
            res.append(TechStackModel(query.value(0),
                                      query.value(1)))

        return res

    def delete(self, id):
        query_text = 'DELETE FROM tech_stacks WHERE id=?'
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(id)

        return query.exec()

    def update(self, data: TechStackModel):
        query_text = "UPDATE tech_stacks SET stack_name=? WHERE id=?"

        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(data.tech_stack)
        query.addBindValue(data.id)

        return query.exec()

    def create(self, data: TechStackModel):
        query_text = 'INSERT INTO tech_stacks (stack_name) VALUES (?)'
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(data.tech_stack)

        return query.exec()


tech_stack_repo_impl = TechStackRepositoryImpl()
