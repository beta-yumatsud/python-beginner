import math

num = 1
name = 'mike'
is_ok = True

print(num, type(num))
print(name, type(name))
print(is_ok, type(is_ok))

# 違う型にもいけちゃう
num = name
print(num, type(num))

name = '1'

# 型変換
new_num = int(name)
print(new_num, type(new_num))

# num: int とかで型宣言は可能。とはいえ、上記のように違う型に代入とかはできちゃう＞＜

# sepを指定しないと半角スペースになるんだってさ
print('Hi', 'Mike', sep=',', end='\n')

print(17 / 3)
# 整数部分のみは // で取れんだってさ、ヘェ〜
print(17 // 3)

# 下記のようなものや、math関数とかはあるんだっばよ
print(round(3.141515151, 2))
print(math.sqrt(25))

# 下記でパッケージのヘルプ情報も出せるんだってさ
#print(help(math))

# 文字列はシングルクォーとでも、ダブルクォートでも大丈夫。
print('say "I don\'t know"')
# 文字列の前に r をつけるrawデータとみなさせるぜよ
print(r'C:\name\name')

# """の後に \ をつけると次の行から出力的な意味合いになるんすね
print("######")
print("""\
line1
line2
line3\
""")
print("######")
# literalどうしは下記のようにも書ける
literal = ('aaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
           'bbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
print(literal)

# 下記のようにindex指定、slice指定も可能。ただしindex指定で文字列代入とかはできへんよ
word = 'python'
print(word[0])
print(word[-1])
print(word[0:2])

word = 'js' + word[4:]
print(word)
print(len(word))

# 文字列には便利なメソッドが色々あって便利すね
s = 'My name is Mike. Hi, Mike.'
is_start = s.startswith('Mi')
print(is_start)
print(s.find("Mike"))
print(s.count("Mike"))
print(s.replace("Mike", 'Job'))

# こんな書き方できんのか。{0}とか指定するのとと同じ
print('a are {} {} {}'.format(1, 2, 3))
print('My name is {name} {family}.'.format(name='Yuki', family='Matsuda'))
# 3.6から上記は `f-strings` というもので書き換えれるらしい
name = 'Yuki'
family = 'Matsuda'
print(f'My name is {name} {family}!!')

