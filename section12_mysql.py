# Database
# MySQL
# $ brew services start mysql
# $ brew services stop mysql
# $ pip install mysql-connector-python
# $ pip install sqlalchemy
# $ pip install PyMySQL
import mysql.connector
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

# create database
conn = mysql.connector.connect(host='127.0.0.1')
cursor = conn.cursor()
cursor.execute(
    'CREATE DATABASE test_mysql_database'
)

conn = mysql.connector.connect(host='127.0.0.1', database='test_mysql_database')
cursor = conn.cursor()
cursor.execute(
    'CREATE TABLE persons('
    'id int NOT NULL AUTO_INCREMENT,'
    'name varchar(14) NOT NULL,'
    'PRIMARY KEY(id))'
)

cursor.execute('INSERT INTO persons(name) values("MIKE")')
conn.commit()

cursor.execute('SELECT * FROM persons')
for row in cursor:
    print(row)

cursor.execute('UPDATE persons SET name = "Michel" WHERE name = "MIKE"')
cursor.execute('DELETE FROM persons WHERE name = "Michel"')

cursor.close()
conn.close()

# SQLAlchemy
# オブジェクト的に操作をできるのが良き
# 下記のようにecho=Trueで実行しているSQLなどが表示され、memory指定も可能
# engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=True)
engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost/test_mysql_database2', echo=True)
Base = sqlalchemy.ext.declarative.declarative_base()


class Person(Base):
    __tablename__ = 'persons'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(14))


Base.metadata.create_all(engine)

Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

person = Person(name='Mike')
session.add(person)
session.commit()

mike = session.query(Person).filter_by(name='Mike').first()
session.delete(mike)
session.commit()

persons = session.query(Person).all()
for person in persons:
    print(person.id, person.name)

