# 正規表現
import re

# 文字列の先頭で正規表現とマッチするか判定
m = re.match('a.c', 'abc')
print(m)
print(m.group()) # abc

# 文字列を操作して正規表現がどこにマッチするか調べる
m = re.search('a.c', 'test abc test, abc')
print(m)
print(m.span()) # (5, 8)
print(m.group())

# 正規表現にマッチする部分文字列を全て探し出しリストとして返す
m = re.findall('a.c', 'test abc test abc')
print(m)

# 重複しないマッチオブジェクトのイテレータを返す
m = re.finditer('a.c', 'test abc test abc')
print(m)
print([w.group() for w in m])

m = re.match('ab?', 'abb') # ab
print(m)
m = re.match('ab*', 'a') # a
print(m)
m = re.match('ab+', 'a') # None
print(m)
m = re.match('a{2,4}', 'aaa')
print(m)
m = re.match('[a-c]', 'b')
print(m)

# m = re.match('[a-zA-z0-9]', 'h')
# 上記はこれでかける
m = re.match('\w', 'a')
print(m)
# m = re.match('[^a-zA-z0-9]', 'h')
# 上記はこれでかける
m = re.match('\W', 'a') # None
print(m)
# m = re.match('[0-9]', 'h')
# 上記はこれでかける
m = re.match('\d', '4') # None
print(m)
# m = re.match('[^0-9]', 'h')
# 上記はこれでかける
m = re.match('\D', '0') # None
print(m)

m = re.match('a|b', 'b')
print(m)
m = re.match('(abc)+', 'abcabc')
print(m)
m = re.match('\s', ' ')
print(m)
m = re.match('\S', ' ')
print(m)
m = re.match('\*', '*')
print(m)
m = re.search('^abc', 'abc hoge abc')
print(m)
m = re.search('abc$', 'abc hoge abc')
print(m)

# re.groupとre.compilerとre.VERBOSE
RE_STACK_ID = re.compile(r"""
     arn:aws:cloudformation:
     (?P<region>[\w-]+):
     (?P<account_id>[\d]+):
     stack/(?P<stack_name>[\w-]+)/[\w-]+
""", re.VERBOSE)
s1 = ('arn:aws:cloudformation:us-east-2:123456789012:stack/'
     'mystack-mynestedstack-sggfrhxhum7w/f449b250-b969-11e0-a185-5081d0136786')
s2 = ('arn:aws:cloudformation:us-east-2:123456789012:stack/'
      'mystack-mynestedstack-sggfrhxhum7w/f449b250-b969-11e0-a185-5081d0136786')
# m = re.match(r'arn:aws:cloudformation:(?P<region>[\w-]+):(?P<account_id>[\d]+):stack/(?P<stack_name>[\w-]+)/[\w-]+', s1)
for s in [s1, s2]:
     m = RE_STACK_ID.match(s)
     if m:
          print(m.group())
          print(m.group('region'))
          print(m.group('account_id'))
          print(m.group('stack_name'))

# re.splitの分割とre.compileの置換
s = 'My name is ... darma2'
print(s.split())
# ...を除くには下記のように書ける
p = re.compile(r'\W+')
print(p.split(s))
# 下記は置換(countで指定回数置換)
p = re.compile('(blue|white|red)')
print(p.sub('colour', 'blue socks and red shoes', count=1))
# 下記でマッチした置換した文字列とマッチした数のtupleが返ってくる
print(p.subn('colour', 'blue socks and red shoes'))


def hex_repl(match):
     value = int(match.group())
     return hex(value)

p = re.compile(r'\d')
# このようにマッチした際に何をさせたいかは関数で指定することも可能
print(p.sub(hex_repl, '12345 55 11 test test2'))

# 正規表現のGreedy（よく深いという意味らしい）
# 最小マッチさせたい時は?を付けようぜ的な話
s = '<html><head><title>Title</title></head></html>'
print(re.match('<.*?>', s))

# format表記
print('{2}, {1} {0}'.format('a', 'b', 'c'))
print('{name} {family}'.format(name='nancy', family='brown'))
t = (1, 2, 3)
print('{0[0]}'.format(t))
print('{t[0]}, {t[1]}'.format(t=t))
print('{0} {2}'.format(*t))
d = {'name': 'anderson', 'family': 'darma2'}
print('{name} {family}'.format(**d))
# 下記で0埋めとかは使えそうかしら？
print('{:<30}'.format('left'))
print('{:>30}'.format('right'))
print('{:^30}'.format('center'))
# :の前はindex, :のあとはどのように表示するか
print('{0:*^30}'.format('center'))
print('{name:{fill}{align}{width}}'.format(name='center', fill='*', align='^', width=30))
# お金のカンマ区切り
print('{:,}'.format(1234567890))
# 数字周りの表示（+,-表示、パーセント表示
print('{:+f} {:+f}'.format(3.14, -3.14))
print('{:.2%}'.format(19/22)) # 86.36%
# 2進数, 8進数とかの表記
print('{0:d}, {0:#x}, {0:#b}'.format(100))
print('{0:d}, {0:x}, {0:b}'.format(100))
for i in range(20):
     for base in 'bdX':
          print('{:5{base}}'.format(i, base=base), end=' ')
     print()

# reprとstr
# representation表示
# pythonオブジェクトとして表示される
print('s')
print(str('s'))
print(repr('s'))

import datetime

d = datetime.datetime.now()
print(d)
print(repr(d))

print('{!r} {} {!s}'.format('test', 'test1', 'test2'))


class Point(object):
     def __init__(self, x, y):
         self.x = x
         self.y = y

     def __repr__(self):
          return 'Point<object>'

     def __str__(self):
          return 'Point ({}, {})'.format(self.x, self.y)


p = Point(10, 20)
print('{0!r} {0} {0!s}'.format(p))

# pprintとjson.dumps
import json
import pprint

l = ['apple', 'orange', 'banana', 'peach']
l.insert(0, l[:])

# ちょっとだけきれいに整形してくれるもの
pp = pprint.PrettyPrinter(indent=4, compact=True)
pp.pprint(l)

# json形式のみやすさ追求パターン（こっちの方が好き）
print(json.dumps(l, indent=4))

# ビット演算子
# pythonで使い機会はあんまないとのこと
# 言語的な意味合いなの、そもそもそんなケースがという話なのかは分からず＞＜
print(0 | 1)
print(1 | 1)
print(0 & 1)
print(1 & 1)
print(0 ^ 1)
print(1 ^ 1)
# 反転
print(~0)
print(~1)
# シフト
print(bin(1))
print(bin(1 << 2))

# Enum
import enum


# 値が一意である場合は下記のデコレータとか付けれる
@enum.unique
class Status(enum.Enum):
     ACTIVE = 1
     INACTIVE = 2
     RUNNING = 3
     # ACTIVATED = ACTIVE


print(Status.ACTIVE)
print(repr(Status.ACTIVE))
print(Status.ACTIVE.name)
print(Status.ACTIVE.value)
for s in Status:
     print(s)
     print(type(s))

db = {
     "stack1": 1,
     "stack2": 2
}
# enum.IntEnumとかも使えそう
# これを使えば下記はTrueになる
print(Status.ACTIVE == 1)

if Status(db['stack1']) == Status.ACTIVE:
     print("shutdown")
elif Status(db["stack2"]) == Status.INACTIVE:
     print("terminate")


class Permission(enum.IntFlag):
     R = 4
     W = 2
     X = 1

print(repr(Permission.R | Permission.W))
RWX = Permission.R | Permission.W | Permission.X
print(Permission.W in RWX)

# functools.lru_cacheとmemoize
# 一時的なcache扱い的な感じ
def momoize(f):
     memo = {}
     def _wrapper(n):
          if n not in memo:
              memo[n] = f(n)
              print("hit memory")
              print(memo)
          return memo[n]
     return _wrapper

@momoize
def long_func(n):
     r = 0
     for i in range(100000):
          r += n * i
     return r

for i in range(10):
     print(long_func(i))

# ただしpython3ではmomoizeではなくlru_cacheを使うと良い
import functools

# maxsizeの指定（要はどの程度cacheするか）も指定可能
@functools.lru_cache()
def long_func2(n):
     r = 0
     for i in range(100000):
          r += n * i
     return r

for i in range(10):
     print(long_func2(i))

# 下記でcacheのクリアもできるよ
# long_func2.cache_clear()
print("next run")
for i in range(10):
     print(long_func2(i))
print(long_func2.cache_info())

# functools.wraps
def d(f):
     # 下記とすることで、helpとかにexample側のdocsが表示できる
     @functools.wraps(f)
     def w():
          """ Wrapper docstring"""
          print("decorator")
          return f()
     return w

@d
def example():
     """ Example docstring"""
     print("example")

example()
help(example)

# functools.partial
def task(f):
     print("start")
     print(f())

# クロージャー
def outer(x, y):
     def inner():
          return x + y
     return inner

f = outer(10, 20)
task(f)

# これをもう少し簡単にかける
def pf(x, y):
     return x + y

p = functools.partial(pf, 10, 20)
task(p)

