from threading import Thread

class Message:

    def __init__(self, ts, is_ack, accept, done):
        self.ts = ts
        self.count = 0
        self.is_ack = is_ack
        self.accept = accept
        self.done = done
