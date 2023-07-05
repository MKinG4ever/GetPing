import time
import ping3
import random
import os
from platform import system
from sys import argv


class GetPing:
    """
        GetPing v0.2
        author: NightFox
        release: 7/5/2023
        see help as GetPing.help() for more information
    """

    def __init__(self):
        # Default IP/PORT
        self.ip = '127.0.0.1'  # default ip/port for monitoring mode feature (no effect on get_ping)
        self.port = 80  # default port
        # Default value
        self.count = 5  # default count number (effect on list_ping)
        self.timeout = 3  # default timeout (effect on ping, get_ping, list_ping)
        self.version = 'GetPing v0.2'  # version information

    def __repr__(self):
        return f'{self.repr}ID:{id(self)}'  # rePresentation

    # Class presentation
    @property
    def repr(self):
        return f'{self.version}\n{self.ip}[:{self.port}] \t (timeout={self.timeout} | count={self.count})\n'

    # get/read the file
    @staticmethod
    def get_file(path):
        with open(path, 'r') as f:
            file = f.readlines()
        return file

    # interrupt function
    @staticmethod
    def delay(sec=None):
        time.sleep(sec) if sec else time.sleep(random.random() / 3.14159265)

    # modify input
    @staticmethod
    def question(quest, answer):
        """make sure answer is not ''(empty str) or just ' '(spaces)"""
        print(f'Default: ({answer})')
        q = input(quest).strip()
        if q and q != answer:
            answer = q
        return answer

    # calculator function
    @staticmethod
    def calc(ip, port, pings):
        # calculating Part
        p = [i for i in pings if isinstance(i, float)]
        send = len(pings)
        received = len(p)
        lost = send - received
        avg = minimum = maximum = None
        if p:  # if received:
            minimum = min(p)
            maximum = max(p)
            avg = sum(p) / len(p)
        # presentation Part
        print(f'Send:{send} / Received:{received} / Lost:{lost}')
        print(f'avg:{avg:.3} / min:{minimum:.3} / max:{maximum:.3}\n') if p else print('- OUT OF RANGE\n')
        return {'ip': ip, 'port': port, 'pings': pings, 'send': send, 'received': received, 'lost': lost,
                'avg': avg, 'min': minimum, 'max': maximum}

    # turn file to readable <ip>:<port> list
    def true_ip(self, path):
        file = self.get_file(path)
        f = []
        for line in file:
            f.append(line.strip().split(':'))
        # f = [line.strip().split(':') for line in self.get_file(path)]
        return f

    # core function
    def ping(self, ip):
        return ping3.ping(dest_addr=ip, timeout=self.timeout)  # set default timeout

    # main function
    def get_ping(self, ip, port, count=1):
        pings = []
        for _ in range(1, count + 1):
            print(f'[{_:3}] {ip}[:{port}] ... ', end='')
            p = self.ping(ip)
            pings.append(p)
            print(f'{p:.3}') if isinstance(p, float) else print(f'{p}')
        # pings = [self.ping(ip) for _ in range(count)]
        return self.calc(ip, port, pings)

    # ping ip s from list
    def list_ping(self, path):
        file = self.true_ip(path)
        result = []
        for line in file:
            r = self.get_ping(line[0], line[1], self.count)  # set default count number
            result.append(r)
        # result = [self.get_ping(line[0], line[1], self.count) for line in file]
        return result

    # reset default values
    def wizard(self):
        # you can use '<IP>' or 'self.ip' for answer.
        # Default IP/PORT
        self.ip = self.question('ip: ', '127.0.0.1')  # default ip/port for monitoring mode
        self.port = int(self.question('port: ', 80))
        # Default values
        self.count = int(self.question('count number: ', 5))
        self.timeout = int(self.question('timeout: ', 3))
        self.version = 'GetPing BetaVersion.'

    # feature
    def validation(self):
        pass

    # help / manual
    def help(self):
        print(self.repr)
        for module in GetPing().__dir__():
            if not module.startswith('_'):
                n = f'GetPing().{module}'
                print(f'GetPing().{module:10} \t | {type(eval(n))}')
        print('see github page for more.\n')
        print('- true_ip() upgraded.')
        print('- list_ping() upgraded.')
        print('- calc() upgraded.')
        print('- get_ping() upgraded.')
