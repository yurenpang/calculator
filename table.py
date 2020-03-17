from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
engine = create_engine('sqlite:///./test.db', echo=True)
meta = MetaData()

students = Table(
   'calculations', meta,
   Column('id', Integer, primary_key = True),
   Column('ip', String(20)),
   Column('text', String(60)),
)

meta.create_all(engine)