import asyncio
import collections


class CountServer(object):
    def __init__(self):
        self.counter = collections.Counter()
        self.lock = asyncio.Lock()

    async def handle_echo(self, reader, writer):
        data = await reader.read()
        name = data.decode()

        async with self.lock:
            if self.counter[name] > 10:
                writer.write(b'-1')
                self.counter[name] = 0
            else:
                writer.write(str(self.counter[name]).encode())
                self.counter[name] += 1
        await writer.drain()
        writer.close()


loop = asyncio.get_event_loop()
counter_server = CountServer()
coro = asyncio.start_server(
    counter_server.handle_echo, "127.0.0.1", 8888, loop=loop
)
server = loop.run_until_complete(coro)
print("server: {}".format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()

