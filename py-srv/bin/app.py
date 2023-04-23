import bottle
from bottle import route, run, static_file
from bottle.ext.sqlalchemy import SQLAlchemyPlugin

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import settings
from model import Base, PopModel

# engine = create_engine('sqlite:///:memory:', echo=True)
engine = engine = create_engine(
    '{engine}://{username}@{host}:{port}/{db_name}'.format(
        **settings.COCKROACH
    ),
    echo=settings.SQLALCHEMY['debug']
)
session_local = sessionmaker(
    bind=engine,
    autoflush=settings.SQLALCHEMY['autoflush'],
    autocommit=settings.SQLALCHEMY['autocommit']
)

@route('/pop')
def get_all_pop(db):
    beverages = db.query(PopModel)
    results = [
        {
            "id": pop.id,
            "name": pop.name,
            "color": pop.color
        } for pop in beverages]

    return {"results": results}

bottle.install(SQLAlchemyPlugin(engine, Base.metadata, create=False, create_session = session_local))

run(host='0.0.0.0', port=8000,debug=True)
