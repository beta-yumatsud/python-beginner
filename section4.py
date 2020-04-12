l = list('abcdefg')
print(l)

# 1つ飛ばしとかもいけんのかー
print(l[::2])

# nestも可能
n = [1, 2, 3, 4, 5]

x = [l, n]
print(x)
print(x[0][3])
print(x[1][-1])

# xに渡しているのは参照になるから、xで出力しても変更されてる
n[0] = 10
print(x)

# 左辺よりオーバーした数で指定すると追加される（エラーにならんのかい）
l[0:2] = ['A', 'B']
print(x)
# 空にできる
l[2:4] = []
print(x)

# appendで末尾に、insertで指定した箇所に
n.append(100)
n.insert(0, 1000)
print(x)
# popで末尾から取り出す（index指定でも取り出せる）
print(n.pop())
print(x)
# delで指定のところから消せる
del n[0]
print(x)
# 指定の値を消すためにはremove（値がないとエラーが返る）
n.remove(2)
print(x)

# 結合
a = [1, 2, 3, 4, 5]
b = [6, 7, 8, 9, 10]
x = a + b
print(x)
# 拡張
a += b
print(a)
x.append(l)
print(x)

# listのメソッド
r = [1, 2, 3, 4, 5, 1, 2, 3]
# index（位置）を教えてくいれる(2つ目の引数はそこから後ろと言う意味）
print(r.index(3, 3))
# countで指定の値がいくつあるか
print(r.count(3))

if 5 in r:
    print('exist')

# sort
r.sort()
print(r)
r.sort(reverse=True)
print(r)
r.reverse()
print(r)

# 結合、分割
s = 'My name is Mike.'
to_split = s.split(' ')  # 存在しないものでやると文字列がただ入るだけ
print(to_split)
print(' '.join(to_split))
# print(help(list))

# copy
# 下記だと参照渡しになるおー
i = [1, 2, 3, 4, 5]
j = i
j[0] = 100
print('j = ', j)
print('i = ', i)
# これでコピー
k = i.copy()
# k = i[:] # これでも同じだが（渡りにくいのcopyを使う）
k[0] = 0
print('k = ', k)
print('i = ', i)
print('i id = ', id(i))
print('j id = ', id(j))
print('k id = ', id(k))

# タプル型(新しい値を入れることを許容しない）
# indexとかt[-1]とかcountはlistと一緒だが、
# removeとかappendとかはない
# immutableな状態にしたいとかに使える！（書き換え不可的なね）
t = (1, 2, 3, 4, 1, 2)
# t = 1, 2, 3 # これも上で同じ
# t = 1, # これもタプル型になる
# t = (1) # これはタプルにならないので注意
# t = (1, 2, 3) + (4, 5, 6) # 新しくは作れるお
print(t)
print(type(t))
# タプルの中にlistを入れて、そのlistは操作可能
tt = ([1, 2, 3], [4, 5, 6])
print(tt)
tt[0][0] = 100
print(tt)

# unpacking tuple
num_tuple = (10, 20)
x, y = num_tuple
print(x, y)
# 下記はtuple型からunpackingされる形になる
min, max = 0, 100
print(min, max)
# 値の置き換えとかにtupleのunpackingは使える
i = 10
j = 20
print(i, j)
i, j = j, i
print(i, j)

# 辞書型
d = {'x': 10, 'y': 20}
print(d)
print(type(d))
print(d['x'])
d['x'] = 100
print(d)
d['x'] = 'XXXX'
print(d)
# 追加は新しくキーを指定すればOK
# キーの型も自由すぎてフォー
d['z'] = 200
print(d)
d[1] = 1
print(d)
print(dict(a=10, b=20))

# 辞書型のメソッド
#print(help(dict))
print(d.keys())
print(d.values())
# updateで同じキーは更新やキーの追加ができるんだわいなー
d2 = {'x': 1000, 'j': 500}
d.update(d2)
print(d)
print(d.get('x'))
print(d.get('xxx')) # ないキーを指定すると、None(non type)が返る
# popで取り出し、delで削除とかはlistと同じ
# clearメソッドで中身をすっきりさせれる
print(d)
print('x key value is', d.pop('x'))
del d['y']
print(d)
d.clear()
print(d)
d = {'a': 10, 'b': 20}
if 'a' in d:
    print('exist a in d')

# 辞書型も参照渡しなので要注意
# コピーしたい場合はlist同様copyを使えば良い

# 集合型
a = {1, 2, 2, 3, 4, 4, 4, 5, 6}
print(a)
print(type(a))
b = {2, 3, 3, 6, 7}
print(b)
print(a - b)
print(b - a)
print(a & b) # and
print(a | b) # or
print(a ^ b) # xor
# 集合型のメソッド
# indexの指定とかはない（なぜなら並びとかがないので）
a.add(10)
print(a)
a.add(10) # 集合なので同じものをaddしても増えはしないお
print(a)
a.remove(10)
print(a)
a.clear()
print(a) # dict型と区別をつけるために空の場合はset()と表示される

# listからの型変換も可能
f = ['apple', 'banana', 'apple', 'banana']
print(f)
kind = set(f)
print(kind)
