# $ pip install pyzmq
import zmq

context = zmq.Context()
# PULL
# sock = context.socket(zmq.PULL)
# SUB
sock = context.socket(zmq.SUB)
sock.setsockopt(zmq.SUBSCRIBE, b'sub1:')
sock.connect("tcp://127.0.0.1:5690")

while True:
    message = sock.recv()
    print("Received: {}".format(message.decode()))
