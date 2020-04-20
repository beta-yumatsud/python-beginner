# コマンドライン引数
# sysパッケージのargvで取得可能
import sys

for arg in sys.argv:
    print(arg)

# init.pyがないとモジュールとして読み込めないよ！
# パッケージとモジュール
# 下記のどちらでもOK（ルールは会社によって違う
# asは名前が長い時とかのみに使うようにする良い
# import lesson_package.tools
from lesson_package.tools import utils as u
from lesson_package.talk import human
from lesson_package.talk import animal
# 上記2つを下記のようにかける
# ただし、__init__に__all__に追記とかは必要
# これもあまり勧められていない（どのモジュールが読み込まれるかわからないので）
# from lesson_package.talk import *

# fromやimportもtry-exceptでImportErrorを掴める
# これは、バージョンが異なる場合などに使える模様
try:
    from lesson_package import utils
except ImportError:
    from lesson_package.tools import utils

# print(lesson_package.utils.say_twice('Hello'))
print(u.say_twice('Hello'))

print(human.sing())
print(human.cry())

print(animal.sing())
print(animal.cry())

# IDEのtoolsから「create setup.py」で公開するパッケージ情報をいい感じに生成できる
# その後にtoolsから「Run setup.py task」を実行するとtarで固めたりして公開できたりする
# python setup.py sdist とかでも良い

# 組み込み関数（pythonに組み込んであるもの）
# https://docs.python.org/ja/3/library/functions.html
# import builtins としているの一緒（明示的にはしないけど）
print(globals())

ranking = {
    'A': 100,
    'B': 85,
    'C': 95
}
# sortedの第2引数にやってほしいこと（下記だと取得したバリューの値で）を指定、
print(sorted(ranking, key=ranking.get, reverse=True))

# 標準ライブラリ
# https://docs.python.org/ja/3/library/index.html
# collections
s = 'fkadfkakjkjkajfkadajfdjalkjkwfofunf'
d = {}
for c in s:
    d.setdefault(c, 0)
    d[c] += 1
print(d)
# これをcollectionsを使うと下記のように書けたりする
from collections import defaultdict

d = defaultdict(int)
for c in s:
    d[c] += 1
print(d)

# importする際の記述方法
# 下記の順で書くのが良いとされちうれ
# 標準パッケージ
# 3rdライブラリ
# 自分たちのチームライブラリ
# localのライブラリ
# かつそこにはスペースを開けて書くのが良いとされている
# かつ、それぞれで、アルファベット順に記載されるのが良いとされる
# 下記のsys.pathでどこから読み込んでいるかを確認すると良い（順番なども注意）
print(sys.path)

# __name__と__main__
# importするだけで実行されしまうものもあるので注意
import config

print(__name__)


# 実際に書く場合は、下記のように書くこと！
# こうすればimportされただけで実行されるといったことは避けれる
def main():
    animal.sing()


if __name__ == '__main__':
    main()


