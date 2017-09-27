from threading import Thread
# TODO: fica a opção no option e ai fica mandando td pra quem n quer mais usar o recurso

class Message:

    def __init__(self, ts, is_ack, accept):
        self.ts = ts
        self.count = 0
        self.is_ack = is_ack
        self.accept = accept
