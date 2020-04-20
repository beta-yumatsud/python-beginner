# 絶対パス
from lesson_package.tools import utils
# 相対パス
# ただしあまり勧められてねぇっす
# from ..tools import utils


def sing():
    return 'sing'


def cry():
    return utils.say_twice('cry')

