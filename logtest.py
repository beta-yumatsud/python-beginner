import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 下記でファイル指定をloggerにも使えるよ
# ロギングハンドラーもいろいろあるので、公式ドキュメントみてみるとおyい
# h = logging.FileHandler('logtest.log')
# logger.addHandler(h)


def do_something():
    logging.info('from log test info')
    logging.debug('from log test debug')

