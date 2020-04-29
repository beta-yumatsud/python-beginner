# Flask
# Web Framework
# 他にもdjangoなどあるがこれを覚えておけば大体一緒だよーとのこと
# $ pip install flask
# hot reloadつきなの助かる
import sqlite3

from flask import Flask
from flask import g
from flask import render_template
from flask import request

app = Flask(__name__)


# DB接続
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('dist/test_flask.db')
    return db


# セッションが切れたら自動で接続をきるてきなやつ
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# GET
@app.route('/')
def hello_world():
    return 'hello world'


@app.route('/roger')
@app.route('/roger/<username>')
def hello_roger(username=None):
    # return 'Hello my Roger!! with {}'.format(username)
    return render_template('hello.html', username=username)


# POST
# 下記のように、requestの中にはすでにFlaskがゴニョゴニョして、
# 値とかを渡してくれているみたい
@app.route('/post', methods=['POST', 'PUT', 'DELETE'])
def show_post():
    return str(request.values)


# DB保存のサンプル
@app.route('/employee', methods=['POST', 'PUT', 'DELETE'])
@app.route('/employee/<name>', methods=['GET'])
def employee(name=None):
    db = get_db()
    curs = db.cursor()
    curs.execute(
        'CREATE TABLE IF NOT EXISTS persons('
        'id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING)'
    )
    db.commit()

    name = request.values.get('name', name)
    if request.method == 'GET':
        curs.execute('SELECT * FROM persons WHERE name = "{}"'.format(name))
        person = curs.fetchone()
        if not person:
            return "No", 404
        user_id, name = person
        return '{}:{}'.format(user_id, name), 200

    if request.method == 'POST':
        curs.execute('INSERT INTO persons(name) values("{}")'.format(name))
        db.commit()
        return 'created {}'.format(name), 201

    if request.method == 'PUT':
        # 下記のようのvaluesで指定すると、値を指定していなければエラーを返すようになる
        new_name = request.values['new_name']
        curs.execute('UPDATE persons SET name = "{}" WHERE name = "{}"'.format(new_name, name))
        db.commit()
        return 'updated {}: {}'.format(name, new_name), 200

    if request.method == 'DELETE':
        curs.execute('DELETE FROM persons WHERE name = "{}"'.format(name))
        db.commit()
        return 'deleted {}'.format(name), 200

    curs.close()


def main():
    app.debug = True
    app.run()


if __name__ == '__main__':
    main()
