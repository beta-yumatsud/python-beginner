# 並列化
# マルチスレッドとマルチプロセス

# プロセス
# Lock〜BarrierまではThreadと同じような形で使える
from multiprocessing import (
    Process,
    Lock, RLock, Semaphore, Queue, Event, Condition, Barrier,
    Value, Array, Pipe, Manager
)
import logging
import multiprocessing
import time

import concurrent.futures

# 下記でスレッド名を出してくれるようにする
logging.basicConfig(level=logging.DEBUG, format='%(processName)s: %(message)s')


def worker_process1():
    logging.debug('start')
    time.sleep(3)
    logging.debug('end')


def worker_process2(x, y=1):
    logging.debug('start')
    logging.debug(x)
    logging.debug(y)
    time.sleep(2)
    logging.debug('end')


def worker_pool(i):
    logging.debug('start')
    time.sleep(3)
    logging.debug('end')
    return i*i


def worker_lock1(d, lock):
    with lock:
        i = d['x']
        time.sleep(2)
        d['x'] = i + 1
        logging.debug(d)


def worker_lock2(d, lock):
    with lock:
        i = d['x']
        time.sleep(2)
        d['x'] = i + 1
        logging.debug(d)


def f(conn):
    conn.send(['test'])
    conn.close()


def f2(num, arr):
    logging.debug(num)
    num.value += 1.0
    logging.debug(arr)
    for i in range(len(arr)):
        arr[i] *= 2


def f_manaegr(l, d, n):
    l.reverse()
    d['x'] += 1
    n.y += 1


if __name__ == '__main__':
    i = 10
    t1 = multiprocessing.Process(target=worker_process1)
    t1.daemon = True
    t2 = multiprocessing.Process(name='renamed worker2',
                                 target=worker_process2, args=(100, ), kwargs={'y': 200})
    t1.start()
    t2.start()
    t2.join()
    t1.join()

    # ワーカープロセスのプールで非同期
    # Poolとapply_asyncを使うだけで良いのか楽ちん
    # poolでセットした値分だけプロセスの数を設定可能
    with multiprocessing.Pool(3) as p:
        p1 = p.apply_async(worker_pool, (100, ))
        p2 = p.apply_async(worker_pool, (200, ))
        logging.debug('executed')
        logging.debug(p1.get(timeout=10))
        logging.debug(p2.get())

    # ワーカープロセスのプールでブロックする際はapplyを使えばOK
    with multiprocessing.Pool(3) as p:
        logging.debug(p.apply(worker_pool, (200, )))
        logging.debug('executed apply')
        p1 = p.apply_async(worker_pool, (100, ))
        p2 = p.apply_async(worker_pool, (200, ))
        logging.debug('executed')
        logging.debug(p1.get(timeout=10))
        logging.debug(p2.get())

    # ワーカープロセスを上記のように書いてたが、下記のようにmapとしてかける
    # こうすることで、並列に実行したものの全ての結果が返ってきたら〜的なことができる
    # map_asyncとgetを使うと、同じようなことも可能
    # imapを使うとiteratorで取得できるので、それをforループで取得とかも可能
    with multiprocessing.Pool(3) as p:
        r = p.map(worker_pool, [100, 100])
        ra = p.map_async(worker_pool, [100, 200])
        logging.debug('executed')
        logging.debug(r)
        logging.debug(ra.get(timeout=10))

        ri = p.imap(worker_pool, [100, 200])
        for i in ri:
            logging.debug(i)

    # プロセス間通信
    # forkでプロセスをコピーしているので、下記では期待通りの動作にはならない
    d = {'x': 0}
    lock = multiprocessing.Lock()
    t1 = multiprocessing.Process(target=worker_lock1, args=(d, lock))
    t2 = multiprocessing.Process(target=worker_lock2, args=(d, lock))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    logging.debug(d)

    # パイプ
    # parent_connからsendとするchild_connのrecvで受け取れる
    parent_conn, child_conn = multiprocessing.Pipe()
    p = multiprocessing.Process(target=f, args=(parent_conn, ))
    p.start()
    logging.debug(child_conn.recv())

    # プロセス間のメモリ共有
    # 下記のようにValueとかArrayを使うと、プロセスセーフで共有できる
    num = multiprocessing.Value('f', 0.0)
    arr = multiprocessing.Array('i', [1, 2, 3, 4, 5])

    p1 = multiprocessing.Process(target=f2, args=(num, arr))
    p2 = multiprocessing.Process(target=f2, args=(num, arr))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    logging.debug(num.value)
    logging.debug(arr[:])

    # マネージャー
    # ちょっと速度が遅くなる見たい
    with multiprocessing.Manager() as manager:
        l = manager.list()
        d = manager.dict()
        n = manager.Namespace()

        l.append(1)
        l.append(2)
        l.append(3)
        d['x'] = 0
        n.y = 0

        p1 = multiprocessing.Process(target=f_manaegr, args=(l, d, n))
        p2 = multiprocessing.Process(target=f_manaegr, args=(l, d, n))
        p1.start()
        p2.start()
        p1.join()
        p2.join()

        logging.debug(l)
        logging.debug(d)
        logging.debug(n)

    # 別マシンで走るプロセス間のネットワーク越しの共有
    # section15_server、section15_client1、section15_client2を参考

    # 高水準のインターフェース(プロセス)
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
        args = [2, 5, 3]
        r = executor.map(worker_pool, *args)
        logging.debug(r)
        logging.debug([i for i in r])




