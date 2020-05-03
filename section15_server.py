import queue

from multiprocessing.managers import BaseManager

q = queue.Queue()


class QueueManager(BaseManager):
    pass


QueueManager.register('get_queue', callable=lambda: q)


manager = QueueManager(address=('127.0.0.1', 5000), authkey=b'hogehogeanderson')
server = manager.get_server()
server.serve_forever()

