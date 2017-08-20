import json

import tornado

import config
import momoko
import sqlalchemy.sql
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.sqltypes import DateTime, NullType, String


class StringLiteral(String):
    """Teach SA how to literalize various things."""

    def literal_processor(self, dialect):
        super_processor = super(StringLiteral, self).literal_processor(dialect)

        def process(value):
            if isinstance(value, int):
                return str(value)
            if not isinstance(value, str):
                value = str(value)
            result = super_processor(value)
            if isinstance(result, bytes):
                result = result.decode(dialect.encoding)
            return result
        return process


class JsonLiteral(StringLiteral):
    """Teach SA how to literalize various things."""

    def literal_processor(self, dialect):
        super_processor = super(JsonLiteral, self).literal_processor(dialect)

        def process(value):
            return super_processor(json.dumps(value))
        return process


class LiteralDialect(postgresql.dialect):
    colspecs = {
        # prevent various encoding explosions
        String: StringLiteral,
        # teach SA about how to literalize a datetime
        DateTime: StringLiteral,
        # don't format py2 long integers to NULL
        NullType: StringLiteral,
        postgresql.INET: StringLiteral,
        postgresql.JSONB: JsonLiteral,
    }


class Service:

    class base:

        def execute(self):
            sql = self.compile(dialect=LiteralDialect(), compile_kwargs={
                               "literal_binds": True}, inline=True)
            res = yield Service.db.execute(str(sql))
            res = res.fetchall()
            return res

    class select(base, sqlalchemy.sql.selectable.Select):
        pass

    class insert(base, sqlalchemy.sql.dml.Insert):
        pass

    class delete(base, sqlalchemy.sql.dml.Delete):
        pass

    class update(base, sqlalchemy.sql.dml.Update):
        pass


def ServiceInit():
    db = momoko.Pool(**config.DB_SETTING)
    future = db.connect()
    tornado.ioloop.IOLoop.instance().add_future(
        future, lambda f: tornado.ioloop.IOLoop.instance().stop())
    tornado.ioloop.IOLoop.instance().start()
    Service.db = db
