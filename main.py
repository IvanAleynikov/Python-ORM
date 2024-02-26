import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from Models import create_tables, Publisher, Shop, Book, Stock, Sale


DSN = "postgresql://postgres:postgres@localhost:5432/ORM_db"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures/tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

Publisher_name = input('Введите имя издателя или его идентификатор: ')

if Publisher_name.isdigit():
    q = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Sale.stock)\
        .join(Book).join(Shop).join(Publisher).filter(Publisher.id == Publisher_name).all()
    for result in q:
        print(f'{result[0]} | {result[1]} | {result[2]} | {result[3]}')
else:
    q = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Sale.stock) \
        .join(Book).join(Shop).join(Publisher).filter(Publisher.name == Publisher_name).all()
    for result in q:
        print(f'{result[0]} | {result[1]} | {result[2]} | {result[3]}')