"""下記を使いながら
pep8 は軽めのチェック
pip install pep8
flake8 はちょっと厳し目のチェック
pip install flake8
pylintは厳しいチェック
pip install pylint
"""

# コードスタイル(IDEの設定や上記ツールで自動的に検知するようにしておこ)
# lineの長さ: 80文字以内
# 無駄な丸括弧とかは付けないのが良いみたい
# indent(tab)は4つのspaceにすること
# =の列を揃えるとかはしない（goとかは揃えるけどpythonは不要）
# global で class とか methodを宣言するときは2行あける、import後もそうみたい
# 文字連結などはメモリ管理の動きを意識すること（他の言語と同じスネ）※下記のlong_wordのように
# シングルクォーテーションを使うのかダブルを使うのかは決めっのお話し
# TODO (アカウント or email) のようにtodoを書くみたいよ
# class名はキャメルケース、関数とか変数はスネークケース
# propertyにするときはアノテーション(@property)を付けてgetとかは付けない
# グローバル変数は全て大文字のスネークケース


def test_func(x, y, z):
    """

    :param x:
    :param y:
    :param z:
    :return:

    Note:
        https://〜のURLは80文字超えても良い
    """


long_word = []
for word in ['fadsjlj', 'fkdf', 'faslfa']:
    long_word.append("{}!!".format(word))
print(''.join(long_word))


# importされただけで実行さないように、メインお実行とかは下記のように書く


def main():
    print("これはメインだぞ")


if __name__ == '__main__':
    main()


# generatorを使う方がメモリ上高速みたい
def t():
    # num = []
    for i in range(10):
        yield i
        # num.append(i)


for i in t():
    print(i)


# lambdaは下記のような小さく適宜せずにかけるときに使おう
def other_func(f):
    print(f(10))


other_func(lambda x: x * 2)
other_func(lambda x: x * 5)

y = None
# y = 'hogehoge'
x = 1 if y else 2
print(x)

# 関数のリスト渡し（参照渡し）はバグに繋がるので再度ご注意をば！再度ですが！
# クロージャーも便利なので再掲載的な(グローバル変数を隠蔽できて、書き換えられたくない時など）
# デコレーターもクロージャーを内部的に利用している感じで、
# 昔のコードではアノテーションなしだったみたい（今はアノテーションで書くのが普通）


def base(x):
    def plus(y):
        return x + y
    return plus


plus = base(10)
print(plus(10))
print(plus(50))

# ドキュメントとPylint
# 英語でドキュメントを書くときはGoogle Translatorを使えば的なこと言っててよかったw
# クラスや関数のドキュメントはダブルクォートで書くよー(というのも再掲載）
# pylintはやや厳しいので、完璧にでなくするとかはしなくても良いおー

