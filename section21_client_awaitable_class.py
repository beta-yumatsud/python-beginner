import asyncio

loop = asyncio.get_event_loop()


# clientで書いた形式は、下記のようにクラスと特殊メソッドでかける
class AwaitableClass(object):
    def __init__(self, name, loop):
        self.name = name
        self.loop = loop

    def __await__(self):
        reader, writer = yield from asyncio.open_connection(
            "127.0.0.1", 8888, loop=self.loop
        )
        writer.write(self.name.encode())
        writer.write_eof()
        # ここにはawaitは描けないので、yield fromを書く
        data = yield from reader.read()
        data = int(data.decode())
        return data


# async forとanext
class AsyncIterater(object):
    def __init__(self, name, loop):
        self.name = name
        self.loop = loop

    def __aiter__(self):
        return self

    async def __anext__(self):
        data = await AwaitableClass(self.name, self.loop)
        if data < 0:
            raise StopAsyncIteration
        return data


# asyncとaenterとaexit
class AsyncContextManater(object):
    def __init__(self, name, loop):
        self.enter = "enter"
        self.ac = AsyncIterater(name, loop)
        self.exit = "exit"

    async def __aenter__(self):
        print(self.enter)
        await asyncio.sleep(3)
        return self.ac

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(self.exit)
        await asyncio.sleep(3)


async def main(name, loop):
    print("chunk reader")
    # result = await AwaitableClass(name, loop)
    async with AsyncContextManater(name, loop) as ac:
        async for i in ac: # AsyncIterater(name, loop):
            print(i)

# blocking関数とかでも、multi processとかで、
# loop.run_in_executorとかで実施すると、並行に実行もできたりする

loop.run_until_complete(asyncio.wait([
    main("task1", loop), main("task2", loop)
]))
loop.close()
