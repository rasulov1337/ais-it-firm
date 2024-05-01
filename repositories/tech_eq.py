from PyQt6.QtSql import QSqlQuery

from repositories.base import BaseRepository, ABC


class TechEqModel:
    def __init__(self,
                 id=0,
                 internet_speed=0,
                 gpu='',
                 cpu='',
                 ram=0):
        self.id = id
        self.internet_speed = internet_speed
        self.gpu = gpu
        self.cpu = cpu
        self.ram = ram


class TechEqRepository(BaseRepository, ABC):
    pass


class TechEqRepositoryImpl(TechEqRepository):
    def get_all(self) -> list[TechEqModel]:
        query_text = 'SELECT * FROM tech_eqs ORDER BY id'
        query = QSqlQuery(self.db)
        query.prepare(query_text)

        if not query.exec():
            exit("Couldn't execute the query!" + self.db.lastError().databaseText())

        res = []
        while query.next():
            res.append(TechEqModel(query.value(0),
                                   query.value(1),
                                   query.value(2),
                                   query.value(3),
                                   query.value(4)))

        return res

    def delete(self, id):
        query_text = 'DELETE FROM tech_eqs WHERE id=?'
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(id)

        return query.exec()

    def update(self, data: TechEqModel):
        query_text = "UPDATE tech_eqs SET internet_speed=?, gpu=?, cpu=?, ram=? WHERE id=?"

        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(data.internet_speed)
        query.addBindValue(data.gpu)
        query.addBindValue(data.cpu)
        query.addBindValue(data.ram)
        query.addBindValue(data.id)

        return query.exec()

    def create(self, data: TechEqModel):
        query_text = 'INSERT INTO tech_eqs (internet_speed, gpu, cpu, ram) VALUES (?, ?, ?, ?)'
        query = QSqlQuery(self.db)
        query.prepare(query_text)
        query.addBindValue(data.internet_speed)
        query.addBindValue(data.gpu)
        query.addBindValue(data.cpu)
        query.addBindValue(data.ram)

        print(query.lastQuery())

        return query.exec()


tech_eq_repo_impl = TechEqRepositoryImpl()
