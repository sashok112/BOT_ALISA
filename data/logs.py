import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Log(SqlAlchemyBase):
    __tablename__ = 'logs'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    status = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)