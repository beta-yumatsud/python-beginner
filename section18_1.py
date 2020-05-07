# Pythonの便利なライブラリやツールや豆知識
# IPython
# pythonの対話型シェルの便利版
# https://ipython.org/documentation.html
# $ pip install ipython
# $ ipython
# %history、%quickrefのようなマジックコマンドがいくつかあって便利ですね

# contextlib
# decoratorに便利
import collections
import contextlib
import csv
import io
import logging
import os
import queue
import re
import requests
import sys
import zipfile


# contextlibを使わない場合
def tag(name):
    def _tag(f):
        def _wrapper(conetnt):
            print('<{}>'.format(name))
            r = f(conetnt)
            print('</{}>'.format(name))
            return r
        return _wrapper
    return _tag


@tag('h2')
def f(content):
    print(content)


f('test of test')


# 上記のものは下記のようにかけちゃう
@contextlib.contextmanager
def tagcc(name):
    print('<{}>'.format(name))
    yield
    print('</{}>'.format(name))


@tagcc('h2')
def fcc(content):
    print(content)


fcc('test of context manager')

# 関数にしなくても、with構文でもかける
with tagcc('h2'):
    print('test of context manager with')
    with tagcc('h5'):
        print('nest of nest')

# contextlibのContextDecorator


class tagClass(contextlib.ContextDecorator):
    def __init__(self, name):
        self.name = name
        self.start_tag = '<{}>'.format(name)
        self.end_tag = '</{}>'.format(name)

    # クラスが一番最初に呼ばれるものらしい
    def __enter__(self):
        print(self.start_tag)

    # クラスの最後に呼ばれるものらしい
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(self.end_tag)


with tagClass('h2'):
    print('こんな書き方でも良いのか')


# contextlib.suppress

try:
    os.remove('hgeohoaggha.tmp')
except FileNotFoundError:
    pass
# 上記のものは下記のように書けちゃう
with contextlib.suppress(FileNotFoundError):
    os.remove('jfkajajfkdjalfd.tmp')

# contextlib.redirect_stdoutとcontextlib.redirect_stderr

# stdin
# x = input('Enter:')
# print(x)

# for line in sys.stdin:
#     print(line)

# stdout
# print('hello')
# sys.stdout.write('hello')

# stderr
# logging.error('Error!!')
# sys.stderr.write('Error!')

# stdoutがredirectされてファイルに書き込まれる
# logを標準出力からファイルへというのもこれだといけそう
with open('dist/stdout.log', 'w') as f:
    with contextlib.redirect_stdout(f):
        print('Hello')

# 上記のstderr版
with open('dist/stderr.log', 'w') as f:
    with contextlib.redirect_stderr(f):
        logging.error("Error!!")

# contextlib.ExistStack


def is_ok_jo():
    try:
        print('do somethin')
        # raise Exception('Error')
        return True
    except Exception:
        return False


def cleanup():
    print('clean up')


# 下記のようなことをもっと簡単にかける
# try:
#     is_ok = is_ok_jo()
#     print('more task')
# finally:
#     if not is_ok:
#         cleanup()
with contextlib.ExitStack() as stack:
    # callbackに入れておくと最終的に実行される
    stack.callback(cleanup)

    @stack.callback
    def cleanup2():
        print('clean up2')

    is_ok = is_ok_jo()
    print('more task')

    if is_ok:
        # ただし、pop_allすると実行されない
        stack.pop_all()

# ioストリーム
# in-memory stream
# ファイルに書くような時にテストや、
# zipファイルをDLして、ファイルには書きこまずにメモリ上で全て実行する
f = io.StringIO()
f.write('string io test')
f.seek(0)
print(f.read())

url = 'https://files.pythonhosted.org/packages/b5/96/af1686ea8c1e503f4a81223d4a3410e7587fd52df03083de24161d0df7d4/setuptools-46.1.3.zip'

f = io.BytesIO()
r = requests.get(url)
f.write(r.content)

with zipfile.ZipFile(f) as z:
    with z.open('setuptools-46.1.3/README.rst') as r:
        print(r.read().decode())

# collections.ChainMap
a = {'a': 'a', 'c': 'c', 'num': 0}
b = {'b': 'b', 'c': 'cc'}
c = {'b': 'bbb', 'c': 'ccc'}

# print(a)
# a.update(b)
# print(a)
# a.update(c)
# print(a)

# 上記のdictが配列で保存される
m = collections.ChainMap(a, b, c)
print(m)
print(m.maps)
print(m['c']) # c
m.maps.reverse()
print(m['c']) # ccc
m.maps.insert(0, {'c': 'ccccccc'})
print(m['c']) # ccc
del m.maps[0]
print(m.maps)
print(m['c']) # ccc
m['b'] = 'BBBBBBB'
print(m.maps)


# 特定の値が大きい場合は入れ替える〜みたいな時に使える
class DeepChainMap(collections.ChainMap):
    def __setitem__(self, key, value):
        for mapping in self.maps:
            if key in mapping:
                if type(mapping[key]) is int and mapping[key] < value:
                    mapping[key] = value
                return
        self.maps[0][key] = value


m = DeepChainMap(a, b, c)
m['num'] = -1
print(m['num']) # 0
m['num'] = 1
print(m['num']) # 1

# collections.defaultdict
d = {}
l = ['a', 'a', 'a', 'b', 'b', 'c']
for word in l:
    d.setdefault(word, 0)
    print(d)

d = collections.defaultdict(int)
for word in l:
    d[word] += 1
print(d)

# 集合にも使える
d = collections.defaultdict(set)
s = [('red', 1), ('blue', 2), ('blue', 4), ('red', 3), ('blue', 4)]
for k, v in s:
    d[k].add(v)
print(d)


# collections.Counter
# このカウンターは便利だな
c = collections.Counter()
for word in l:
    c[word] += 1
print(c)
# 大きい順で2位まで出してくれる
print(c.most_common(2))
print(sum(c.values()))

with open('section18_1.py', 'r') as f:
    words = re.findall(r'\w+', f.read().lower())
    print(collections.Counter(words).most_common(10))

# collections.deque
# Double-end queue
# listとdequeの違いは、dequeはメモリ上効率的に操作可能（高速）
# queueはマルチスレッドとかで使う
q = queue.Queue()
lq = queue.LifoQueue()
l = []
d = collections.deque()

for i in range(3):
    q.put(i)
    lq.put(i)
    l.append(i)
    d.append(i)

for _ in range(3):
    print('FIFO queue = {}'.format(q.get()))
    print('LIFO queue = {}'.format(lq.get()))
    print('list       = {}'.format(l.pop()))
    print('deque      = {}'.format(d.pop()))

# dequeは下記のようにindexでもアクセス可能
# print(d[1])
d.extendleft('x')
d.extend('y')
d.extendleft('u')
print(d)
d.rotate()
print(d)
d.clear()
print(d)

# collections.namedtuple
# 下記は通常のtuple
p = (10, 20)
print(p[0])

# クラスみたいな形でtupleを作れる（値を書き換えれないフィールドを持たせる的な）
Point = collections.namedtuple('Point', ['x', 'y'])
p = Point(x=10, y=20)
print(p.x)

# _makeのように明示的にtupleと分かるようにする方法もある
p1 = Point._make([100, 200])
print(p1)
print(p1._asdict())
# 下記はコピー的な感じ
p2 = p1._replace(x=500)
print(p1)
print(p2)


class SumPoint(collections.namedtuple('Point', ['x', 'y'])):
    @property
    def total(self):
        return self.x + self.y


p3 = SumPoint(2, 3)
print(p3.x, p3.y, p3.total)

import io
import logging
import os
import queue
import re
import requests
import sys
import zipfile


# contextlibを使わない場合
def tag(name):
    def _tag(f):
        def _wrapper(conetnt):
            print('<{}>'.format(name))
            r = f(conetnt)
            print('</{}>'.format(name))
            return r
        return _wrapper
    return _tag


@tag('h2')
def f(content):
    print(content)


f('test of test')


# 上記のものは下記のようにかけちゃう
@contextlib.contextmanager
def tagcc(name):
    print('<{}>'.format(name))
    yield
    print('</{}>'.format(name))


@tagcc('h2')
def fcc(content):
    print(content)


fcc('test of context manager')

# 関数にしなくても、with構文でもかける
with tagcc('h2'):
    print('test of context manager with')
    with tagcc('h5'):
        print('nest of nest')

# contextlibのContextDecorator


class tagClass(contextlib.ContextDecorator):
    def __init__(self, name):
        self.name = name
        self.start_tag = '<{}>'.format(name)
        self.end_tag = '</{}>'.format(name)

    # クラスが一番最初に呼ばれるものらしい
    def __enter__(self):
        print(self.start_tag)

    # クラスの最後に呼ばれるものらしい
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(self.end_tag)


with tagClass('h2'):
    print('こんな書き方でも良いのか')


# contextlib.suppress

try:
    os.remove('hgeohoaggha.tmp')
except FileNotFoundError:
    pass
# 上記のものは下記のように書けちゃう
with contextlib.suppress(FileNotFoundError):
    os.remove('jfkajajfkdjalfd.tmp')

# contextlib.redirect_stdoutとcontextlib.redirect_stderr

# stdin
# x = input('Enter:')
# print(x)

# for line in sys.stdin:
#     print(line)

# stdout
# print('hello')
# sys.stdout.write('hello')

# stderr
# logging.error('Error!!')
# sys.stderr.write('Error!')

# stdoutがredirectされてファイルに書き込まれる
# logを標準出力からファイルへというのもこれだといけそう
with open('dist/stdout.log', 'w') as f:
    with contextlib.redirect_stdout(f):
        print('Hello')

# 上記のstderr版
with open('dist/stderr.log', 'w') as f:
    with contextlib.redirect_stderr(f):
        logging.error("Error!!")

# contextlib.ExistStack


def is_ok_jo():
    try:
        print('do somethin')
        # raise Exception('Error')
        return True
    except Exception:
        return False


def cleanup():
    print('clean up')


# 下記のようなことをもっと簡単にかける
# try:
#     is_ok = is_ok_jo()
#     print('more task')
# finally:
#     if not is_ok:
#         cleanup()
with contextlib.ExitStack() as stack:
    # callbackに入れておくと最終的に実行される
    stack.callback(cleanup)

    @stack.callback
    def cleanup2():
        print('clean up2')

    is_ok = is_ok_jo()
    print('more task')

    if is_ok:
        # ただし、pop_allすると実行されない
        stack.pop_all()

# ioストリーム
# in-memory stream
# ファイルに書くような時にテストや、
# zipファイルをDLして、ファイルには書きこまずにメモリ上で全て実行する
f = io.StringIO()
f.write('string io test')
f.seek(0)
print(f.read())

url = 'https://files.pythonhosted.org/packages/b5/96/af1686ea8c1e503f4a81223d4a3410e7587fd52df03083de24161d0df7d4/setuptools-46.1.3.zip'

f = io.BytesIO()
r = requests.get(url)
f.write(r.content)

with zipfile.ZipFile(f) as z:
    with z.open('setuptools-46.1.3/README.rst') as r:
        print(r.read().decode())

# collections.ChainMap
a = {'a': 'a', 'c': 'c', 'num': 0}
b = {'b': 'b', 'c': 'cc'}
c = {'b': 'bbb', 'c': 'ccc'}

# print(a)
# a.update(b)
# print(a)
# a.update(c)
# print(a)

# 上記のdictが配列で保存される
m = collections.ChainMap(a, b, c)
print(m)
print(m.maps)
print(m['c']) # c
m.maps.reverse()
print(m['c']) # ccc
m.maps.insert(0, {'c': 'ccccccc'})
print(m['c']) # ccc
del m.maps[0]
print(m.maps)
print(m['c']) # ccc
m['b'] = 'BBBBBBB'
print(m.maps)


# 特定の値が大きい場合は入れ替える〜みたいな時に使える
class DeepChainMap(collections.ChainMap):
    def __setitem__(self, key, value):
        for mapping in self.maps:
            if key in mapping:
                if type(mapping[key]) is int and mapping[key] < value:
                    mapping[key] = value
                return
        self.maps[0][key] = value


m = DeepChainMap(a, b, c)
m['num'] = -1
print(m['num']) # 0
m['num'] = 1
print(m['num']) # 1

# collections.defaultdict
d = {}
l = ['a', 'a', 'a', 'b', 'b', 'c']
for word in l:
    d.setdefault(word, 0)
    print(d)

d = collections.defaultdict(int)
for word in l:
    d[word] += 1
print(d)

# 集合にも使える
d = collections.defaultdict(set)
s = [('red', 1), ('blue', 2), ('blue', 4), ('red', 3), ('blue', 4)]
for k, v in s:
    d[k].add(v)
print(d)


# collections.Counter
# このカウンターは便利だな
c = collections.Counter()
for word in l:
    c[word] += 1
print(c)
# 大きい順で2位まで出してくれる
print(c.most_common(2))
print(sum(c.values()))

with open('section18_1.py', 'r') as f:
    words = re.findall(r'\w+', f.read().lower())
    print(collections.Counter(words).most_common(10))

# collections.deque
# Double-end queue
# listとdequeの違いは、dequeはメモリ上効率的に操作可能（高速）
# queueはマルチスレッドとかで使う
q = queue.Queue()
lq = queue.LifoQueue()
l = []
d = collections.deque()

for i in range(3):
    q.put(i)
    lq.put(i)
    l.append(i)
    d.append(i)

for _ in range(3):
    print('FIFO queue = {}'.format(q.get()))
    print('LIFO queue = {}'.format(lq.get()))
    print('list       = {}'.format(l.pop()))
    print('deque      = {}'.format(d.pop()))

# dequeは下記のようにindexでもアクセス可能
# print(d[1])
d.extendleft('x')
d.extend('y')
d.extendleft('u')
print(d)
d.rotate()
print(d)
d.clear()
print(d)

# collections.namedtuple
# 下記は通常のtuple
p = (10, 20)
print(p[0])

# クラスみたいな形でtupleを作れる（値を書き換えれないフィールドを持たせる的な）
Point = collections.namedtuple('Point', ['x', 'y'])
p = Point(x=10, y=20)
print(p.x)

# _makeのように明示的にtupleと分かるようにする方法もある
p1 = Point._make([100, 200])
print(p1)
print(p1._asdict())
# 下記はコピー的な感じ
p2 = p1._replace(x=500)
print(p1)
print(p2)


class SumPoint(collections.namedtuple('Point', ['x', 'y'])):
    @property
    def total(self):
        return self.x + self.y


p3 = SumPoint(2, 3)
print(p3.x, p3.y, p3.total)

# 使い所としてcsvファイルの取り扱い
# 簡単にcsvファイルをクラスのように取り扱える
with open('dist/names.csv', 'w') as csvfile:
    fieldnames = ['first', 'last', 'address']
    w = csv.DictWriter(csvfile, fieldnames=fieldnames)
    w.writeheader()
    w.writerow({'first': 'Mike', 'last': 'Jackson', 'address': 'a'})
    w.writerow({'first': 'Jun', 'last': 'Sakai', 'address': 'a'})
    w.writerow({'first': 'Nancy', 'last': 'Mask', 'address': 'a'})

with open('dist/names.csv', 'r') as f:
    csv_reader = csv.reader(f)
    Names = collections.namedtuple('Names', next(csv_reader))
    for row in csv_reader:
        names = Names._make(row)
        print(names)

# dict型の入れた順序を保証したければ, collections.OrderedDictを使う方が良い
# 3.6以降に順序通りになったが、完全に保証はしていない
od = collections.OrderedDict({'banana': 3, 'apple': 1, 'orange': 2})
d = {'banana': 3, 'apple': 1, 'orange': 2}
# 一緒にはなる
print(od == d)
# sortedを使うとkeyで指定した内容の順序を覚えてくれている
od = collections.OrderedDict(
    sorted(d.items(), key=lambda t : t[0])
)
print(od)
# これだと一番最後に入る
od['candy'] = 99
print(od)

