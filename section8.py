# ファイルの作成
# wだと上書き、aだと追記
# 下記のようにwithステートメントを使うと、
# インデント内の処理が全て終わると勝手にcloseしてくれる
# このように何か処理が終わったら最後に何かするなどによく使われるみたい
with open('test.txt', 'w') as f:
    f.write('test\n')
    # printで書き込めるのは便利だな＞＜(とはいえ、f.writeを使う方が多いみたい)
    print('I am print', file=f)
    print('My', 'name', 'is', 'Mike', sep='#', end='!', file=f)
# f.close()

# ファイルの読み込み
with open('test.txt', 'r') as f:
    # 下記だと全て読み込み
    # print(f.read())

    while True:
        # chunk単位で読み込む場合は下記のようにする
        # chunk = 2
        # line = f.read(chunk)
        # 下記で1行1行読み込まれる
        line = f.readline()
        print(line, end='')
        if not line:
            break

with open('test.txt', 'r') as f:
    # telで現在の位置がわかる
    print(f.tell())
    print(f.read(1))
    # seekで位置の移動
    f.seek(5)
    print(f.read(1))
    f.seek(15)
    print(f.read(1))
    f.seek(0)
    print(f.read(1))

# ファイルの読み込み書き込み
# w+で書き込み読み込み
# wで開くと最初にファイルが空の状態で書き込みモードになるので注意
# r+だと最初にファイルが読み込めないとエラーになる(事前にファイルが必要)
s = """\
AAA
BBB
CCC
DDD
"""
with open('test2.txt', 'w+') as f:
    f.write(s)
    # 書き込んだら先頭に戻らないと読み込みは最後からとか途中からになる
    f.seek(0)
    print(f.read())

import string
# ファイルテンプレート
# stringのTemplateでテンプレートとして使える
# htmlとかに変数を埋め込む的な形で使える
ss = """\
Hi $name.

$contents

Have a good day.
"""

t = string.Template(ss)
contetns = t.substitute(name='Mike', contents="How are you?")
print(contetns)

# withを使った場合は下記のtはwithの外でも使えるよ！
with open('design/email_template.txt', 'r') as f:
    t = string.Template(f.read())
contetns = t.substitute(name='Mike', contents="How are you?")
print(contetns)

# csvファイル
import csv
with open('test.csv', 'w') as csv_file:
    fieldnames = ['Name', 'Count']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'Name': 'A', 'Count': 1})
    writer.writerow({'Name': 'B', 'Count': 2})

with open('test.csv', 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        print(row['Name'], row['Count'])

# ファイル操作
import os

print(os.path.exists('test.txt'))
print(os.path.isfile('test.txt'))
print(os.path.isdir('design'))
# renameとかsymlinkとかも下記でできるよ
# os.rename('test.txt', 'renamed.txt')
# os.symlink('renamed.txt', 'symlink.txt')
# os.mkdir('test_dir')
# rmdirはディレクトリにファイルがあると消せない
# os.rmdir('test_dir')
# より便利なライブラリとしてpathlibがある
import pathlib
pathlib.Path('empty.txt').touch()
os.remove('empty.txt')
print(os.listdir('lesson_package'))
# pathlib.Path('test_dir/test_dir2/empty.txt').touch()

# print(glob.glob('test_dir/test_dir2/*'))
# globを使うとディレクトリの中の全てのファイルを〜とかも可能
import glob
print(glob.glob('lesson_package/talk/*'))

# import shutil
# shutil.copy('lesson_package/talk/animal.py', 'lesson_package/tools/animal.py')
# shutil.rmtree('test_dir')

print(os.getcwd())

# tarfileの圧縮と展開
import tarfile

with tarfile.open('dist/test.tar.gz', 'w:gz') as tr:
    # 下記で圧縮
    tr.add('lesson_package')

with tarfile.open('dist/test.tar.gz', 'r:gz') as tr:
    # 展開するには下記のコマンド
    # tr.extractall(path='dist/test_dir')
    # 下記では展開せずに中身を見ることができる
    with tr.extractfile('lesson_package/__init__.py') as f:
        print(f.read())

# zipfileの圧縮と展開
import zipfile

with zipfile.ZipFile('dist/test.zip', 'w') as z:
    # 下記だとファイルを1つ1つ指定する必要ある
    # z.write('lesson_package')
    # 下記のようにglobを使えば良い
    for f in glob.glob('lesson_package/**', recursive=True):
        print(f)
        z.write(f)

with zipfile.ZipFile('dist/test.zip', 'r') as z:
    # z.extractall('hoge')
    with z.open('lesson_package/__init__.py') as f:
        print(f.read())

# tempfile
# 使い終わったら勝手に消してくれるんだってさ
import tempfile

with tempfile.TemporaryFile(mode='w+') as t:
    t.write('Hello')
    t.seek(0)
    print(t.read())

# 下記だと消さずに残せる
with tempfile.NamedTemporaryFile(delete=False) as t:
    print(t.name)
    with open(t.name, 'w+') as f:
        f.write('test\n')
        f.seek(0)
        print(f.read())

# 下記でtempディレクトリ
# 内部的には tempfile.mkdtemp()を実行するのと同じ
with tempfile.TemporaryDirectory() as d:
    print(d)

# subprocessでコマンドを実行する
import subprocess

subprocess.run(['ls', '-al'])
# 下記はセキュリティ的によくないので使わない方が良いみたい
# subprocess.run('ls -al | grep test', shell=True)
# 下記で結果も受け取れる
# r = subprocess.run('ls -al | grep test', shell=True, check=True)

# 下記のようにするとパイプを使うことも可能だよ
# p1 = subprocess.Popen(['ls', '-la'], stdout=subprocess.PIPE)
# p2 = subprocess.Popen(['grep', 'test'], stdin=p1.stdout, stdout=subprocess.PIPE)
# p1.stdout.close()
# output = p2.communicate()[0]
# print(output)

# datetime
# これは使う機会が多そう
import datetime

now = datetime.datetime.now()
print(now)
print(now.isoformat())
print(now.strftime('%d/%m/%y-%H%M%S%f'))

# これで今日とか取れるのか
today = datetime.datetime.today()
print(today)
print(today.isoformat())
print(today.strftime('%d/%m/%y'))

# 自分なりの時間を作れる
t = datetime.time(hour=1, minute=10, second=5, microsecond=100)
print(t)
print(t.isoformat())
print(t.strftime('%H_%M_%S_%f'))

# 1週間前とかも扱える
# daysとかhoursとかminutesとかもあるのよー
d = datetime.timedelta(weeks=-1)
print(now + d)

import time
print('#####')
time.sleep(2)
print('#####')

# 下記でエポックタイムを使える
time.time()

# 下記のようにすると、バックアップファイルとして作成とかもねできちゃうよね
import shutil
file_name = 'test.txt'
if os.path.exists(file_name):
    shutil.copy(file_name, "{}.{}".format(file_name, now.strftime('%d/%m/%y-%H%M%S%f')))

with open(file_name, 'w') as f:
    f.write('test')

