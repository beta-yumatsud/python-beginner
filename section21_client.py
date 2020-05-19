import asyncio

loop = asyncio.get_event_loop()


async def request_server(name, loop):
    reader, writer = await asyncio.open_connection(
        "127.0.0.1", 8888, loop=loop
    )
    writer.write(name.encode())
    writer.write_eof()
    data = await reader.read()
    data = int(data.decode())
    return data


async def main(name, loop):
    print("chunk reader")
    result = await request_server(name, loop)
    print(result)


loop.run_until_complete(asyncio.wait([
    main("task1", loop), main("task2", loop)
]))
loop.close()

