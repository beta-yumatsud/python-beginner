# DBM
import dbm

# dbmはstringがbyteしか保存できないっす
with dbm.open('cache', 'c') as db:
    db['key1'] = 'value1'
    db['key2'] = 'value2'

with dbm.open('cache', 'r') as db:
    print(db.get('key1'))

# memcache
# $ brew install memcached
# $ pip install python-memcached
# $ /usr/local/opt/memcached/bin/memcached -vv
import memcache

db = memcache.Client(['127.0.0.1:11211'])
db.set('web_page', 'value1', time=30)
page = db.get('web_page')
if page:
    # cacheでヒットしなかったらそのまま返して
    print(page)
    # ヒットしなかったらdbから取得して、cacheに入れておく
    # 的なデファクトなこともできるよーという紹介だった

db.set('counter', 0)
db.incr('counter', 1)
db.incr('counter', 1)
db.incr('counter', 1)
db.incr('counter', 1)
print(db.get('counter'))

# pickle
# pythonのデータをそのまま保存するもの
# 使いどころによっては便利な気もする
import pickle


class T(object):

    def __init__(self, name):
        self.name = name

data = {
    'a': [1, 2, 3],
    'b': {'test', 'test'},
    'c': {'key': 'value'},
    'd': T('test')
}

with open('data.pickle', 'wb') as f:
    pickle.dump(data, f)

with open('data.pickle', 'rb') as f:
    data_loaded = pickle.load(f)
    print(data_loaded)
    print(data_loaded['d'].name)
