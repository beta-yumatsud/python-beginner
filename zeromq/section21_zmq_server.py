import time

import zmq

context = zmq.Context()
# 1回だけ実行されるものの場合はPUSH&PULL
# sock = context.socket(zmq.PUSH)
# 複数の場合はPUB/SUB
sock = context.socket(zmq.PUB)
sock.bind("tcp://127.0.0.1:5690")

id = 0
while True:
    id += 1
    # sock.send(str(id).encode())
    sock.send(("sub1:" + str(id)).encode())
    print("Sent: {}".format(id))
    time.sleep(1)

