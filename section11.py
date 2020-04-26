# config parser
"""
[DEFAULT]
debug = False

[web_server]
host = 127.0.0.1
port = 80

[db_server]
host = 127.0.0.1
port = 3306
"""
import configparser

config = configparser.ConfigParser()
config['DEFAULT'] = {
    'debug': True
}
config['web_server'] = {
    'host': '127.0.0.1',
    'port': 80
}
config['db_server'] = {
    'host': '127.0.0.1',
    'port': 3306
}

with open('config.ini', 'w') as config_file:
    config.write(config_file)

config = configparser.ConfigParser()
config.read('config.ini')
print(config['web_server'])
print(config['db_server'])

# yaml file
import yaml

with open('config.yml', 'w') as yaml_file:
    yaml.dump({
        'web_server': {
            'host': '127.0.0.1',
            'port': 80
        },
        'db_server': {
            'host': '127.0.0.1',
            'port': 3306
        }
    }, yaml_file, default_flow_style=False)

with open('config.yml', 'r') as yaml_file:
    data = yaml.load(yaml_file)
    print(data, type(data))

# logging
# 通常はWARNING以上のみ出力
# logging.basicConfigでログレベルを変更
# ログフォーマットは公式ドキュメントを確認すること！
"""CRITICAL, ERROR, WARNING, INFO, DEBUG"""
import logging

formatter = '%(levelname)s:%(asctime)s:%(message)s'
logging.basicConfig(level=logging.DEBUG, format=formatter)
# logging.basicConfig(filename='test.log', level=logging.DEBUG)

logging.critical('critical')
logging.error('error')
logging.warning('warning')
logging.info('info {}'.format('test'))
logging.debug('debug %s %s', 'test', 'test')

# logger: ログレベルをファイル単位で変えて出力できたりするよ
# loggerを指定しないと、基本的にはroot扱いになる
# mainでbasicConfigを設定し、他ではloggerを使って設定・出力するのが良い
# かつ、各ファイルなりでは先頭でloggerの設定をする
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.debug('debug')

# logger handler
import logtest

logtest.do_something()

# logging filter
# logging.Filterクラスを継承してfilterを独自に定義すれば良き


class NoPassFilter(logging.Filter):
    def filter(self, record):
        log_message = record.getMessage()
        return 'password' not in log_message


logger = logging.getLogger(__name__)
logger.addFilter(NoPassFilter())
logger.info('from main')
logger.info('from main password: test')

# logging config
# configの設定方法は公式ドキュメントを読みなよyou!!
# それを logging.config.fileConfig('logging.ini') とかで読み込む
# もしくは setting.py で logging.config.dictConfig でdict形で設定も可能

# loggingの書き方
# この辺はモニタリングの形式に合わせて出力すると良い
# あとはトラブル対応の時にどこにどうあると良いか（センス！）
# 下記のようにdict型を指定することもの可能

logger.error({
    'action': 'create',
    'status': 'fail',
    'message': 'Api call is failed'
})

# e-mail送信
from email import message
from email.mime import multipart
from email.mime import text
import smtplib

smtp_host = 'smtp.live.com'
smtp_port = 587
from_email = 'hogehoge@hotmail.com'
to_email = 'fugafuga@hotmail.com'
username = 'hogehoge@hotmail.com'
password = 'hogehoge'

# msg = message.EmailMessage()
msg = multipart.MIMEMultipart()
# msg.set_content('Test email')
msg['Subject'] = 'Test email sub'
msg['From'] = from_email
msg['To'] = to_email
msg.attach(text.MIMEText('Test email', 'plain'))

with open('section11.py', 'r') as f:
    attachment = text.MIMEText(f.read(), 'plain')
    attachment.add_header(
        'Content-Disposition', 'attachment',
        filename='lesson.txt'
    )
    msg.attach(attachment)

# server = smtplib.SMTP(smtp_host, smtp_port)
# server.ehlo()
# server.starttls()
# server.ehlo()
# server.login(username, password)
# server.send_message(msg)
# server.quit()
# メール送信先プロバイダーによってルールが異なるので注意

# SMTPハンドラーでログをemail送信
# 上記でやったloggerのaddHandlerでlogging.handlers.SMTPHandlerを使う

# virtualenv
# ex. Pythonの複数環境を使いたいなど
# IDEで設定も可能だし、コマンドでも可能
# $ virtualenv my_python_env で新しく作成
# $ source my_python_env/bin/activate で指定した環境になる
# $ deactivate でdefault環境に戻る

# option parse
# sysで受け取れたオプションの高機能版
from optparse import OptionParser
from optparse import OptionGroup


def main():
    """
    $ python section11.py -f test.txt --num=1000 a b -v
    """
    usage = 'usage: %prog [options] arg1 arg2'
    parser = OptionParser(usage=usage)
    parser.add_option('-f', '--file', action='store', type='string',
                      dest='filename', help='File name')
    parser.add_option('-n', '--num', action='store', type='int', dest='num')
    parser.add_option('-v', action='store_false', dest='verbose', default=True)

    # 下記のように-rをつけると、指定の値が入るとかもできる
    parser.add_option('-r', action='store_const', const='root', dest='user_name')

    # callback
    parser.add_option('-e', dest='env')
    def is_releas(option, opt_str, value, parser):
        if parser.values.env == 'prd':
            raise parser.error('Can not release')

    parser.add_option('--release', action='callback', callback=is_releas, dest='release')

    # 下記でgroupingも可能
    group = OptionGroup(parser, 'Dangerous options')
    group.add_option('-g', action="store_true", help='Group option')
    parser.add_option_group(group)

    options, args = parser.parse_args()
    print(options)
    print(options.filename)
    print(options.num)
    print(options.verbose)
    print(args)


if __name__ == '__main__':
    main()


