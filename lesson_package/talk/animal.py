# 絶対パス
from lesson_package.tools import utils
# 相対パス
# ただしあまり勧められてねぇっす
# from ..tools import utils


def sing():
    return '##hohokfkldafdjlksing'


def cry():
    return utils.say_twice('jfalsdfjalkcry')


# importされただけで実行されないようにするにはこんな感じで書く
if __name__ == '__main__':
    print(sing())
    print('animal:', __name__)
