# if文はまぁindentで表現するくらいかな
x = -10
y = -10
if x < 0:
    print("negative")
    if y < 0:
        print("negative")
elif x == 0:
    print("zero")
else:
    print("positive")

# debuggerやbreak pointなどはIDEの機能を使えば普通に便利

# pythonには&&とか||はないおー
if x < 0 and y < 0:
    print("very negative")

# 否定はnotを使う、!ではないおー
a = [1, 2, 3, 4, 5]
b = 10
if b not in a:
    print("not in")

# false判定: 数字の0、空の文字列、空の配列、空の辞書型、空のタプル、空の集合
r = []
if r:
    print("OK")
else:
    print("NO")

# nullオブジェクト（None）
# is は型判定的な感じで使えるみたい
is_empty = None
print(type(is_empty))
if is_empty is None:
    print("None!!!")

# while, continue, breakも大体他の言語と同じかな
# ++のよう表現はできない
count = 0
while True:  # count < 5:
    if count >= 5:
        break
    if count == 2:
        count += 1
        continue
    print(count)
    count += 1

# while elseは最後に一回実行したい的な時に使うのかしら。
# 途中にbreakを入れるとelseにはいかない（あくまでelseはwhileの一貫）
count = 0
while count < 5:
    print(count)
    count += 1
else:
    print("done")

# input関数はインタープリター的な感じで対話的なプログラムを作りたい場合は使えるね
while False:  # True:
    word = input("Enter:")
    if word == 'ok':
        break
    print("next")

# for文も大体他のコードと同じ感じだ
num_list = [1, 2, 3, 4, 5]
for num in num_list:
    print(f"num: {num}")
else:
    print("DONE")

# range関数もおんなじかんじだなー
# range(開始位置、終了位置、skip数）
# 終了位置は含まれないみたいね
# _ で使わないと宣言できる見たい
for i in range(2, 11, 2):
    print(i)

# enumerateを使うと、indexとかを付けてくれるみたい、へぇ〜
for i, fruit in enumerate(['apple', 'banana', 'orange']):
    print(i, fruit)

# zip関数は、下記のように配列をいい感じまとめて出してあげる
# ちなみに配列の数が合わない場合は、一番小さい配列に合わさられるみたい
days = ['Mon', 'Tue', 'Wed']
fruits = ['apple', 'banana', 'orange']
drinks = ['coffee', 'tea']
for day, fruit, drink in zip(days, fruits, drinks):
    print(day, fruit, drink)

# zip objectと表示された
print(zip(days, fruits, drinks))

# dict型
d = {'x': 100, 'y': 200}
for k, v in d.items():
    print(f'{k} : {v}')
print(d.items())


# dict_items([('x', 100), ('y', 200)])
# 中身はタプルになってるのかー

# functions
# 引数とか返り値とかは他の言語と同じ感じ(デフォルト引数やキーワード指定引数など）
# 引数も返り値も型宣言とかは可能（結局宣言以外も入れれるので、あまりやらないみたいだけど）
def say_something():
    print("Hi!")
    s = "Hello"
    return s


print(type(say_something))
# f = say_something
result = say_something()
print(result)


def what_is_this(color="white"):
    print(color)


what_is_this("red")
what_is_this()
what_is_this(color="blue")


# Note: Pythonではデフォルト引数で空の配列や辞書型などの参照渡しを指定すべきではない（バグに繋がる）
#def test_func(x, l=[]):
def test_func(x, l=None):
    if l is None:
        l = []
    l.append(x)
    return l


#y = [1, 2, 3]
#r = test_func(100, y)
#print(r)
r = test_func(100)
print(r)
r = test_func(100)
print(r)


# 位置引数のタプル化
# 引数をまとめて（タプル化して）受け取るときは*を付ければよい
def say_something(word, *args):
    print(f'word = {word}')
    for arg in args:
        print(arg)


say_something("Hi", "Mike", "Nance")
t = ("Jon", 'Nancy')
say_something("Hello", *t)


# キーワード引数の辞書化
# 辞書型で渡すときは**を付けてあげる
# 通常の引数、タプル型、辞書型を混ぜて引数に渡すこともできる
# ただし順序は重要(**は最後にするなど)
def menu(**kwargs):
    print(kwargs)
    for k, v in kwargs.items():
        print(f'k={k}, v={v}')


d = {
    'entree': 'beef',
    'drink': 'ice coffee',
    'dessert': 'ice'
}
menu(**d)


# Docstrings
# 関数の説明とかはこんな感じで書くのが良いみたい
def example_func(param1, param2):
    """Example function with types documented in the docstring.

    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.
    """
    print(param1)
    print(param2)
    return True


print(example_func.__doc__)


# 関数内関数とかもいけんぜ
def outer(a, b):
    def plus(c, d):
        return c + d
    r = plus(a, b)
    print(r)


outer(1, 2)


# クロージャー
def circle_area_func(pi):
    def circle_area(radius):
        return pi * radius * radius
    return circle_area


ca1 = circle_area_func(3.14)
ca2 = circle_area_func(3.141592)
# 何かしらやって、その後に使いたい方を使うみたいときとか言う例が出てきた
print(ca1(10))
print(ca2(10))


# デコレーター
# @print_infoのようにするとprint_infoにadd_numが渡されるみたい、へぇ〜
# 関数の前後処理を一度作ってしまい、それを使いまわせるのが便利ね
# 2つ重ねることも可能で、先に記載した方から順に実行される
def print_more(func):
    def wrapper(*args, **kwargs):
        print("func:", func.__name__)
        print("args:", args)
        print("kwargs:", kwargs)
        result = func(*args, **kwargs)
        print("result:", result)
        return result
    return wrapper


def print_info(func):
    def wrapper(*args, **kwargs):
        print("start")
        result = func(*args, **kwargs)
        print("end")
        return result
    return wrapper


@print_info
@print_more
def add_num(a, b):
    return a + b


# f = print_info(add_num)
print(add_num(10, 20))

# ラムダ
# 無名関数とかとして使えるのでこれはコード量減って良さげですね
l = ['Mon', 'tue', 'Wed', 'Thu', 'fri', 'sat', 'Sun']


def change_words(words, func):
    for word in words:
        print(func(word))


# def sample_func(word):
#    return word.capitalize()
# sample_func = lambda word: word.capitalize()
# change_words(l, sample_func)

change_words(l, lambda word: word.capitalize())
change_words(l, lambda word: word.lower())


# ジェネレーター
# 反復処理をする際に1つ1つの処理を生成するのが特徴みたいよ
# for文とかで一気に実行したくない時とかに便利かも
# 小分けにして重たい処理を実装して、都度呼ぶとからしい
l = ['Good morning', 'Good afternoon', 'Good night']
for i in l:
    print(i)
print("######")


def greeting():
    yield "Good morinig"
    yield "Good afternoon"
    yield "Godd night"


def counter(num=10):
    for _ in range(num):
        yield "run"


for g in greeting():
    print(g)

g = greeting()
c = counter()
print(next(g))
print(next(c))
print(next(c))
print(next(c))
print(next(c))
print("@@@@@@")
print(next(g))
print(next(c))
print(next(c))
print(next(c))
print(next(c))
print(next(c))
print("@@@@@@")
print(next(g))
# これ以上呼び出せない！時にはstop iterationと言うエラーが発生するみたいね

# リスト内包表記
# メモリ節約、スピード向上とかに繋がるみたい
# for文1つとかif文1つくらいだと良いみたい
t = (1, 2, 3, 4, 5)
t2 = (5, 6, 7, 8, 9, 10)
r = [i for i in t]
print(r)
r = [i for i in t if i % 2 == 0]
print(r)
r = [i * j for i in t for j in t2]
print(r)

# 辞書内包表記
w = ['mon', 'tue', 'wed']
f = ['coffee', 'milk', 'water']
d = {x: y for x, y in zip(w, f)}
print(d)

# 集合内包表記
s = {i for i in range(10) if i % 2 != 0}
print(s)


# ジェネレーター内包表記
# 書き方がtupleに似てるの注意
g = (i for i in range(10))
print(type(g))
print(next(g))
print(next(g))
print(next(g))
print(next(g))

# 名前空間とスコープ
animal = 'cat'


def f():
    """Test func doc"""
    # 下記の2つのように、local変数宣言前にanimalを使おうとしているとしてエラーになる
    # print(animal)
    # animal = 'dog'
    # ただし、globalで宣言すると、local変数ではなくなるよ！
    animal = 'dog'
    print('local:', locals()) # localで宣言されたものが表示される
    print(f.__name__)
    print(f.__doc__)


f()
print(__name__)
print('global:', globals())

# 例外処理
# 他の言語でいうところのtry-catch-finally
# exceptには何も指定しない(BaseException, 大体はException)と全てのエラーをexceptする
# ただし何も指定しないとか、Exceptionでcatchは他の言語と同様あんましよくないとのこと
# try-finallyとすると、エラーになるが、最後に実行したいものがあるときによく使う場合
# elseは何もerrorがない場合に実行したいことがあるときは記載する！
l = [1, 2, 3]
i = 5
try:
    l[i]
except IndexError as exc:
    print("Don't worry: {}".format(exc))
except NameError as exc:
    print(exc)
except Exception as exc:
    print("other: {}".format(exc))
else:
    print("done")
finally:
    print("clean up")
print("last!!")


# 独自例外
# 下記で例外を発生させれる
# 自分たちなりのエラーを発生させるには独自のものを作ろう
# raise IndexError("test error")


class UppercaseError(Exception):
    pass


def check():
    fruits = ['APPLE', 'banana', 'orange']
    for fruit in fruits:
        if fruit.isupper():
            raise UppercaseError(fruit)


try:
    check()
except UppercaseError as exc:
    print('This is my fault. Go Next.')
