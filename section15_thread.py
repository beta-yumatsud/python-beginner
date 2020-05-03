# 並列化
# マルチスレッドとマルチプロセス

# スレッド
import logging
import queue
import threading
import time

import concurrent.futures

# 下記でスレッド名を出してくれるようにする
logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')


def worker1():
    logging.debug('start')
    time.sleep(3)
    logging.debug('end')


def worker2(x, y = 1):
    logging.debug('start')
    logging.debug(x)
    logging.debug(y)
    time.sleep(2)
    logging.debug('end')


def worker3(d, lock):
    logging.debug('start')
    # withステートメントで書くとreleaseを書かなくてもOK
    lock.acquire()
    i = d['x']
    time.sleep(2)
    d['x'] = i + 1
    logging.debug(d)
    lock.release()
    logging.debug('end')


def worker4(semaphore):
    with semaphore:
        logging.debug('start')
        time.sleep(2)
        logging.debug('end')


def worker5(semaphore):
    with semaphore:
        logging.debug('start')
        time.sleep(2)
        logging.debug('end')


def worker6(semaphore):
    with semaphore:
        logging.debug('start')
        time.sleep(2)
        logging.debug('end')


def workerquere1(queue):
    logging.debug('queue start')
    queue.put(100)
    time.sleep(3)
    queue.put(200)
    logging.debug('queue end')


def workerquere2(queue):
    logging.debug('queue start')
    logging.debug('queue: {}'.format(queue.get()))
    logging.debug('queue: {}'.format(queue.get()))
    # 上記でQueueの中身を取るまで待つみたい、へぇ〜
    logging.debug('queue end')


def workerqueue(queue):
    logging.debug('start!!')
    while True:
        item = queue.get()
        if item is None:
            break
        logging.debug(item)
        # putした数だけtask_doneを呼ばれなければいけない
        queue.task_done()

    logging.debug('longggggggggggggggggg')
    logging.debug('end!!')


def worker_event1(event):
    event.wait()
    logging.debug('event start!!')
    time.sleep(3)
    logging.debug('event end!!')


def worker_event2(event):
    logging.debug('event start!!')
    logging.debug('event end!!')
    event.set()


def worker_cond1(cond):
    with cond:
        cond.wait()
        logging.debug('cond start!!')
        time.sleep(3)
        logging.debug('cond end!!')


def worker_cond2(cond):
    with cond:
        cond.wait()
        logging.debug('cond start!!')
        time.sleep(3)
        logging.debug('cond end!!')


def worker_cond3(cond):
    with cond:
        logging.debug('cond start!!')
        time.sleep(3)
        logging.debug('cond end!!')
        cond.notifyAll()


def worker_barrier1(barrier):
    r = barrier.wait()
    logging.debug('num={}'.format(r))
    while True:
        logging.debug('barrier start!!')
        time.sleep(3)
        logging.debug('barrier end!!')


def worker_barrier2(barrier):
    r = barrier.wait()
    logging.debug('num={}'.format(r))
    while True:
        logging.debug('barrier start!!')
        time.sleep(3)
        logging.debug('barrier end!!')


# どちらが先に終わるかは実行のたびに変わるよ
# MainThreadというものからThreadが作られる
if __name__ == '__main__':
    # Threadのパラメータで何を渡せるのかは中身を見てみると良いよ
    t1 = threading.Thread(name='rename worker1', target=worker1)
    # 下記のようにすると、MainThread側は終了するまで待たなくなる
    t1.setDaemon(True)
    t2 = threading.Thread(target=worker2, args=(100, ), kwargs={'y': 200})
    t1.start()
    t2.start()
    print('start')
    # setDaemonをセットした場合は、下記のようにすると、終了するまで待つ
    t1.join()
    # setDaemonしていなければ、下記のように明示しなくても良いが、そこはCoding Rule次第
    t2.join()

    # 現在動いているThreadのリストはthreading.enumerate()でわかる
    for _ in range(5):
        t = threading.Thread(target=worker1)
        t.setDaemon(True)
        t.start()
    for thread in threading.enumerate():
        if thread is threading.currentThread():
            print(thread)
            continue
        thread.join()

    # timerの設定
    timer = threading.Timer(3, worker2, args=(100, ), kwargs={'y': 200})
    timer.start()
    # 下記のように書く必要もないが、プログラムの実行上わかりやすくするため
    timer.join()

    # LockとRLock
    # 引数として渡してあげて、メソッドないでacquire()とrelease()
    # 2度lockしたいような場合にRLockを使うみたい
    d = {'x': 0}
    lock = threading.Lock()
    t1 = threading.Thread(target=worker3, args=(d, lock))
    t2 = threading.Thread(target=worker3, args=(d, lock))
    t1.start()
    t2.start()
    # 下記のように書く必要もないが、プログラムの実行上わかりやすくするため
    t1.join()
    t2.join()

    # セマフォ
    # lockをかけれるスレッド数を設定できる
    semaphore = threading.Semaphore(2)
    t1 = threading.Thread(target=worker4, args=(semaphore,))
    t2 = threading.Thread(target=worker5, args=(semaphore,))
    t3 = threading.Thread(target=worker6, args=(semaphore,))
    t1.start()
    t2.start()
    t3.start()
    # 下記のように書く必要もないが、プログラムの実行上わかりやすくするため
    t1.join()
    t2.join()
    t3.join()

    # Queue
    q = queue.Queue()
    t1 = threading.Thread(target=workerquere1, args=(q, ))
    t2 = threading.Thread(target=workerquere2, args=(q, ))
    t1.start()
    t2.start()
    # 下記のように書く必要もないが、プログラムの実行上わかりやすくするため
    t1.join()
    t2.join()

    q2 = queue.Queue()
    for i in range(10):
        q2.put(i)
    t1 = threading.Thread(target=workerqueue, args=(q2,))
    t1.start()
    logging.debug('task are not done')
    # 下記でQueueに積んだタスクが全部終わったかどうかを待つ
    # 終わった際に実行したいことがある場合にも使われる
    q2.join()
    logging.debug('task are done')
    q2.put(None)
    t1.join()

    q3 = queue.Queue()
    for i in range(1000):
        q3.put(i)
    ts = []
    for _ in range(3):
        t = threading.Thread(target=workerqueue, args=(q3, ))
        t.start()
        ts.append(t)
    logging.debug('task are not done')
    q3.join()
    logging.debug('task are done')
    for _ in range(len(ts)):
        q3.put(None)

    [t.join() for t in ts]

    # Event
    # producerとconsumer、event drivenのようなことが可能
    event = threading.Event()
    t1 = threading.Thread(target=worker_event1, args=(event, ))
    t2 = threading.Thread(target=worker_event2, args=(event, ))
    t1.start()
    t2.start()
    # 下記のように書く必要もないが、プログラムの実行上わかりやすくするため
    t1.join()
    t2.join()

    # Condition
    # EventとLockの組み合わせ的なイメージ、notifyAllとwaitを使うことで実現可能
    c = threading.Condition()
    t1 = threading.Thread(target=worker_cond1, args=(c, ))
    t2 = threading.Thread(target=worker_cond2, args=(c, ))
    t3 = threading.Thread(target=worker_cond3, args=(c, ))
    t1.start()
    t2.start()
    t3.start()
    # 下記のように書く必要もないが、プログラムの実行上わかりやすくするため
    t1.join()
    t2.join()
    t3.join()

    # バリア
    # 同じ数のスレッドが必要な場合に使えます〜
    barrier = threading.Barrier(2)
    t1 = threading.Thread(target=worker_barrier1, args=(barrier,))
    t2 = threading.Thread(target=worker_barrier2, args=(barrier,))
    t1.start()
    t2.start()
    # 下記のように書く必要もないが、プログラムの実行上わかりやすくするため
    t1.join()
    t2.join()

    # 高水準のインターフェース
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        f1 = executor.submit(worker2, 2, 5)
        f2 = executor.submit(worker2, 2, 5)
        logging.debug(f1.result())
        logging.debug(f2.result())

        args = [[2, 2], [5, 5]]
        r = executor.map(worker2, *args)
        logging.debug(r)
        logging.debug([i for i in r])

