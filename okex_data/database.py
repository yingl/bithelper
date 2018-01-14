import datetime as dt
import traceback
from peewee import BooleanField # peewee相关模块
from peewee import CharField
from peewee import DateTimeField
from peewee import FloatField
from peewee import Model
from peewee import MySQLDatabase
from peewee import TextField

db = MySQLDatabase(host='localhost',
                   user='root',
                   passwd='',
                   database='bithelper',
                   charset='utf8')

class btc_tops(Model):
    data = TextField() # In json format
    updated_at = DateTimeField(default=dt.datetime.now)
    class Meta:
        database = db

class btc_bottoms(Model):
    data = TextField()
    updated_at = DateTimeField(default=dt.datetime.now)
    class Meta:
        database = db

class btc_values(Model):
    code = CharField()
    price = FloatField()
    updated_at = DateTimeField(default=dt.datetime.now)
    class Meta:
        database = db

class btc_k_data(Model):
    data = TextField()
    tag = CharField()
    updated_at = DateTimeField(default=dt.datetime.now)
    class Meta:
        database = db

if __name__ == '__main__':
    try:
        db.connect()
        db.create_tables([btc_tops, btc_bottoms, btc_values, btc_k_data], safe=True)
    except Exception as e:
        print('%s\n%s' % (e, traceback.print_exc()))
    finally:
        if db:
            db.close()
