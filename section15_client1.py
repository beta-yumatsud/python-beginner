from multiprocessing.managers import BaseManager


class QueueManager(BaseManager):
    pass


QueueManager.register('get_queue')
manager = QueueManager(address=('127.0.0.1', 5000), authkey=b'hogehogeanderson')
manager.connect()
queue = manager.get_queue()
queue.put('Hello')
queue.put('Hello')


