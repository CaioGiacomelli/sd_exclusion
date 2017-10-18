import message
import threading
import socket
import pickle
import copy
import os
import time


class MyThread (threading.Thread):

    def __init__(self, accept, pr, is_ack, done):

        threading.Thread.__init__(self)
        self.accept = accept
        self.pr = pr
        self.is_ack = is_ack
        self.done = done
        # self.name = name
        # self.counter = counter

    def run(self):
        send_request(self.accept, self.pr, self.is_ack, self.done)


def send_request(accept, pr, is_ack, done):

    if not accept:
        for j in pr:
            message_ts = str(p[j-1].ts) + str(p[j-1].pid)
            message_ts = int(message_ts)
            print("TS da mensagem enviada: ", message_ts)
            for process in p:
                tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcp.connect((host, process.port))
                m1 = message.Message(message_ts, 0, accept, done)
                m_dumped = pickle.dumps(m1)
                tcp.send(m_dumped)
                tcp.close()
            p[j-1].ts += 1

    elif accept:
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp.connect((host, p[pr - 1].port))
            m1 = message.Message(0, is_ack, 1, done)  # Fazer depois a mensagem ACK ou NACK
            m_dumped = pickle.dumps(m1)
            x = tcp.send(m_dumped)
            tcp.close()


class MyThread2 (threading.Thread):

    def __init__(self, pr):

        threading.Thread.__init__(self)
        self.process = pr
        # self.name = name
        # self.counter = counter

    def run(self):
        Process.receive(self.process)


class Process:

    def __init__(self, pid, host, port):
        self.pid = pid
        self.ts = 1
        self.queue = []
        self.process_list = []
        self.ack = 0
        self.nack = 0
        self.host = host
        self.port = port
        self.recurso = 0
        thread2 = MyThread2(self)
        thread2.start()

    def set_process_list(self, process_list):
        self.process_list = process_list

    def set_recurso(self):
        self.recurso = 1

    def receive(self):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        orig = (self.host, self.port)
        tcp.bind(orig)
        tcp.listen(1)

        while True:

            con, cliente = tcp.accept()

            while True:
                msg = con.recv(1024)
                if msg:
                    msg_loaded = pickle.loads(msg)
                    new_m = copy.copy(msg_loaded)

                if not msg: break

            con.close()
            if not new_m.accept:
                if self.recurso == 1:
                    ts_process = str(self.ts) + str(self.pid)
                    ts_process = int(ts_process)

                    print("processo: ", self.pid, "mensagem ts: ", new_m.ts, " ts_process: ", ts_process)

                    if new_m.ts > ts_process:
                        st = str(new_m.ts)
                        y = st[(len(st) - 1):]
                        x = int(y)

                        if self.pid != x:
                            thread3 = MyThread(1, x, 0, 0)
                            thread3.start()
                            self.queue.append(x)

                        print("Processo ", x, " esta na fila de ", self.pid)



                    if new_m.ts < ts_process:

                        st = str(new_m.ts)
                        y = st[(len(st) - 1):]
                        x = int(y)

                        if self.pid != x:
                            thread3 = MyThread(1, x, 1, 0)
                            thread3.start()

                if self.recurso == 0:
                    st = str(new_m.ts)
                    y = st[(len(st) - 1):]
                    x = int(y)

                    if self.pid != x:
                        print("self.pid: ", self.pid, " x: ", x)
                        thread3 = MyThread(1, x, 1, 0)
                        thread3.start()

            elif new_m.accept:

                if new_m.is_ack:
                    self.ack+=1
                else:
                    self.nack+=1

                ts_process = str(self.ts) + str(self.pid)
                ts_process = int(ts_process)
                if self.ack == (len(self.process_list) - 1) and self.recurso:


                        self.ack = 0
                        self.nack = 0
                        self.recurso = 0

                        for p in self.process_list:
                            ts_p = str(p.ts) + str(p.pid)
                            ts_p = int(ts_p)
                            while(ts_process < ts_p):
                                while ts_p > ts_process:
                                    self.ts += 1
                                    ts_process = str(self.ts) + str(self.pid)
                                    ts_process = int(ts_process)

                        if len(self.queue) != 0:

                            for item in self.queue:
                                thread4 = MyThread(1, item, 1, 1)
                                thread4.start()

                        self.queue = []
                        print("Processo ", self.pid, " utilizou o recurso ", ts_process)

                # elif self.ack == (len(self.process_list) - 1) and new_m.done and self.recurso:
                #     print("Processo ", self.pid, " utilizou o recurso ", self.recurso, self.ack, ts_process)
                #     self.ack = 0
                #     self.nack = 0
                #     self.recurso = 0
                #
                #     for p in self.process_list:
                #         ts_p = str(p.ts) + str(p.pid)
                #         ts_p = int(ts_p)
                #         while (ts_process < ts_p):
                #             while ts_p > ts_process:
                #                 self.ts += 1
                #                 ts_process = str(self.ts) + str(self.pid)
                #                 ts_process = int(ts_process)
                #
                #     for item in self.queue:
                #         thread5 = MyThread(1, item, 1, 1)
                #         thread5.start()
                #
                #     self.queue = []

host = '127.0.0.1'
process_number = 1
p = [Process(process_number, host, 5000), Process(process_number + 1, host, 5001), Process(process_number + 2, host, 5002)]

for proc in p:
    proc.set_process_list(p)

while True:
    print("Digite os processos que desejam utilizar o recurso ou digite sair para fechar o programa")
    option = input()

    if option == 'sair':
        os._exit(0)

    option = [int(i) for i in option.split()]
    for o in option:
        p[o-1].set_recurso()

    thread1 = MyThread(0, option, 0, 0)
    thread1.start()

    time.sleep(0.5)