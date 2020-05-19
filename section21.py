# 非同期処理 asynico
import asyncio
import asyncio.subprocess
import multiprocessing
import threading
import time
import sys

import aiohttp
import requests

def g_hello():
    yield "hello 1"
    yield "hello 2"
    yield "hello 3"
    return "DONE"

def g_hello2():
    # 一時中断して（入力待ち）的なものをジェネレータベースのコルーチンとかいうらしい
    r = yield "Hello!!"
    yield r

def g_hello3():
    while True:
        # yield from で別ジェネレータを呼ぶことができる
        r = yield from g_hello()
        yield r

def worker():
    print("start")
    time.sleep(2)
    print("stop")


loop = asyncio.get_event_loop()


# Python3.6以上であれば、async-awaitのネィティブコルーチンを使える
# @asyncio.coroutine
async def async_worker():
    print("asyncio start")
    # yield from asyncio.sleep(2)
    await asyncio.sleep(2)
    print("asyncio end")


async def hello(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response = await response.read()
            print(response)
            print(time.time())


async def lock_worker(lock):
    print("lock worker start")
    async with lock:
        print("lock!!!")
        await asyncio.sleep(2)
    print("lock worker end")


async def event_worker1(event):
    print("event1 worker start")
    await event.wait()
    print("got event1!!!")
    await asyncio.sleep(2)
    print("event1 worker end")


async def event_worker2(event):
    print("event2 worker start")
    await asyncio.sleep(2)
    print("event2 worker end")
    event.set()

async def condition_worker1(condition):
    async with condition:
        await condition.wait()
        print("condition worker1 start")
        print("got condition!!!")
        await asyncio.sleep(2)
        print("condition worker1 end")

async def condition_worker2(condition):
    async with condition:
        print("condition worker2 start")
        await asyncio.sleep(2)
        print("condition worker2 end")
        condition.notify_all()

async def queue_worker1(queue):
    print("queue worker1 start")
    await asyncio.sleep(2)
    await queue.put(100)
    print("queue worker1 end")

async def queue_worker2(queue):
    print("queue worker2 start")
    x = await queue.get()
    print(x)
    print("queue worker2 end")

async def future_f(future):
    await asyncio.sleep(1)
    future.set_result("Future is done!!")

async def future_callback(future):
    print(future.result())
    loop.stop()

def hello_schedule(name, loop):
    print("hello {}".format(name))
    loop.stop()

async def compute(x, y):
    print("Compute {} + {}...".format(x, y))
    await asyncio.sleep(1.0)
    return x + y

async def print_sum(x, y):
    result = await compute(x, y)
    print("{} + {} = {}".format(x, y, result))

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE
    )
    stdout, strerr = await proc.communicate()
    print(stdout.decode())
    exitcode = await proc.wait()
    print(exitcode)

g = g_hello()
print(next(g))
print(next(g))
print(next(g))

g = g_hello2()
print(next(g))
print(g.send("plus"))
# print(next(g))

g = g_hello3()
print(next(g))
print(next(g))
print(next(g))
print(next(g))
print(next(g))
print(next(g))
print(next(g))

if __name__ == "__main__":
    # マルチスレッド
    t1 = threading.Thread(target=worker)
    t2 = threading.Thread(target=worker)
    t1.start()
    t2.start()

    # マルチプロセス
    p1 = multiprocessing.Process(target=worker)
    p2 = multiprocessing.Process(target=worker)
    p1.start()
    p2.start()

    # asyncio
    loop.run_until_complete(asyncio.wait([async_worker(), async_worker()]))
    # loop.close()

    loop.run_until_complete(asyncio.wait([
        hello("http://httpbin.org/headers"),
        hello("http://httpbin.org/headers")
    ]))
    # loop.close()

    # lock
    lock = asyncio.Lock()
    loop.run_until_complete(asyncio.wait([
        lock_worker(lock),
        lock_worker(lock)
    ]))
    # loop.close()

    # event
    event = asyncio.Event()
    loop.run_until_complete(asyncio.wait([
        event_worker1(event),
        event_worker2(event)
    ]))
    # loop.close()

    # condition
    condition = asyncio.Condition()
    loop.run_until_complete(asyncio.wait([
        condition_worker1(condition),
        condition_worker2(condition)
    ]))

    # Semaphore
    # も上記たちと同様な感じでできる
    # semaphore = asyncio.Semaphore(2)

    # Queue
    queue = asyncio.Queue()
    loop.run_until_complete(asyncio.wait([
        queue_worker1(queue),
        queue_worker2(queue)
    ]))
    # loop.close()

    # Future
    future = asyncio.Future()
    asyncio.ensure_future(future_f(future))
    loop.run_until_complete(future)
    print(future.result())
    # loop.close()

    # コールバックも使える
    # future = asyncio.Future()
    # asyncio.ensure_future(future_f(future))
    # future.add_done_callback(future_callback)
    # loop.run_forever()
    # loop.close()

    # scheduling
    loop.call_later(3, hello_schedule, "Mike", loop)
    # 下記はすぐに実行なので、上記のlaterが完了する前に完了する
    # loop.call_soon(hello_schedule, "Mike", loop)
    loop.run_forever()
    # loop.close()

    # asyncioのチェーン
    loop.run_until_complete(asyncio.wait([
        print_sum(10, 20)
    ]))
    # loop.close()

    # sub process
    loop.run_until_complete(asyncio.wait([
        run("ls -la"), run("date")
    ]))
    loop.close()

    # サーバクライアントのストリーム通信
    # https://docs.python.org/ja/3/library/asyncio-stream.html
