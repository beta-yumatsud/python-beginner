# クラスとオブジェクト
# クラスのメソッド、いちいちselfつけるのめんどい＞＜
# python3だと、objectは不要らしいが、書いておいた方が良いみたい
class Person(object):
    # 初期化(constructor)。初期化時のパラメータなどは通常の関数と同じ
    def __init__(self, name=''):
        self.name = name
        print('First')

    def say_something(self):
        print('Hello,', self.name)
        self.run(num=10)

    def run(self, num):
        print('run' * num)

    # destructor
    def __del__(self):
        print('good bye')

person = Person('Mike')
person.say_something()
# del person とかにしてもdestructorは呼ばれる
# これをしないと、プログラムが終了するまでdestructorは呼ばれない
print('FINISH!!')

# 継承
# 他のプログラム言語と大体同じ
# メソッドのオーバーライドも他の言語と同じイメージでOK
# superで親メソッドの呼び出しなども同じ感じがする
class Car(object):
    def __init__(self, model=None):
        self.model = model

    def run(self):
        print('run')

    def ride(self, person):
        person.drive()

class ToyotaCar(Car):
    pass # こうかくと何もしないんだってさ

class TeslaCar(Car):
    def __init__(self, model='Model S', enable_auto_run=False, password='123'):
        super().__init__(model)
        self._enable_auto_run = enable_auto_run
        self.password = password

    # プロパティには_(アンダーバー)をつける(ただし、これでも読み込みも書き込みも可能)ことで、
    # 書き換えて欲しくないー、かつプロパティを使ってという明示的な意図になるらしい
    # 外からアクセスできないようにするには __ のように2つつける（ただしクラス内では参照可能）
    # 下記のようにすることで、enable_auto_runを書き換え負荷にする（要はgetter）
    @property
    def enable_auto_run(self):
        return self._enable_auto_run

    # こういう書き方をするのは、特定の時だけ書き換えて良いよーなどの時に使うみたい
    @enable_auto_run.setter
    def enable_auto_run(self, is_enable):
        if self.password == '456':
            self._enable_auto_run = is_enable
        else:
            raise ValueError

    def run(self):
        print('super fast run')

    def auto_run(self):
        print('auto run')

car = Car()
car.run()

car = ToyotaCar()
car.run()

tesla_car = TeslaCar('Model S')
print(tesla_car.model)
tesla_car.auto_run()
tesla_car.run()
#tesla_car.enable_auto_run = True
print(tesla_car.enable_auto_run)

# クラスをデータ構造体として扱うときの注意
# オブジェクトを作成してからデータをつけるなどは注意
# tesla_car.__enable_auto_runとかにしちゃうと新しく要素が作成されたことになりバグに繋がるらしい(fmfm)


# ダックタイピング
# オブジェクト指向のお話しだけですた
# 抽象クラス
# 多用しない方が良いみたいなので、必要であれば作る
import abc


class Person2(metaclass=abc.ABCMeta):
    def __init__(self, age=1):
        self.age = age

    @abc.abstractmethod
    def drive(self):
        pass


class Car2(object):
    def __init__(self, model=None):
        self.model = model

    def run(self):
        print('run')

    def ride(self, person):
        person.drive()


class Baby(Person2):
    def __init__(self, age=1):
        if age < 18:
            super().__init__(age)
        else:
            raise ValueError

    def drive(self):
        raise Exception('No drive')


class Adult(Person2):
    def __init__(self, age=18):
        if age >= 18:
            super().__init__(age)
        else:
            raise ValueError

    def drive(self):
        print('OK')

baby = Baby()
adult = Adult()

car = Car2()
car.ride(adult)
adult.drive()

# 多重継承
# 継承先で同じメソッドがある場合は、先に継承している（左側）ものが優先される
class PersonCarRobot(Person, Car2):
    def fly(self):
        print('fly')

person_car_robot = PersonCarRobot()
person_car_robot.say_something()
person_car_robot.fly()

# クラス変数
# 下記のようにselfを付けないでおくと全てのオブジェクトで使える(共有される)変数になる
# その変数は本当に共通なので、リストなどは共有するとオブジェクト間で変更されてバグに繋がる
# そういう場合はselfでオブジェクト毎で分けること
class PersonClass(object):
    kind = 'human'

    def __init__(self, name):
        self.name = name

    def who_are_you(self):
        print(self.name, self.kind)

    @classmethod
    def what_is_your_kind(cls):
        return cls.kind

    @staticmethod
    def about(year):
        print('about human {}'.format(year))

a = PersonClass('A')
a.who_are_you()
b = PersonClass('B')
b.who_are_you()

# クラスメソッドとスタティックメソッド
# クラスは()を付けないとオブジェクトではなくクラスとして扱われれる
# @classmethod, 引数にclsとしてあげるとクラスメソッドとして使える
# @staticmethodとするとスタティックメソッドになる（あんまり使わないかもとのこと）
c = PersonClass("hoge")
print(c.name)
b = PersonClass
print(b.kind)
print(b.what_is_your_kind())
print(PersonClass.kind)
print(PersonClass.what_is_your_kind())
print(PersonClass.about(2020))

# 特殊メソッド
# __hogehoge__などが特殊メソッド
class Word(object):
    def __init__(self, text):
        self.test = text

    def __str__(self):
        return 'Word!!!!!'

    def __len__(self):
        return len(self.test)

    def __add__(self, word):
        self.test.lower() + word.test.lower()

    def __eq__(self, other):
        return self.test.lower() == other.test.lower()

w = Word('test')
w2 = Word('#########')
print(w)
print(len(w))
print(w + w2)
print(w == w2)
