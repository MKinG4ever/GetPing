import time
import ping3
import random
import os
from platform import system
from sys import argv


class GetPing:
    """
        GetPing v0.1
        author: NightFox
        release: 7/4/2023
        see help as GetPing.help() for more information
    """

    def __init__(self):
        self.ip = '127.0.0.1'  # default ip for monitoring mode feature (no effect on get_ping)
        self.port = 80  # default port for monitoring mode feature (no effect on get_ping)
        self.count = 3  # default count number
        self.timeout = 3  # default timeout

    def __repr__(self):
        return f'{self.repr}'  # rewrite Presentation

    @property
    def repr(self):
        return f'GetPing v0.1\n{self.ip}[:{self.port}] \t (timeout={self.timeout} | count={self.count})'

    # get ip s from file
    @staticmethod
    def get_file(path):
        with open(path, 'r') as f:
            file = f.readlines()
        return file

    # turn every line of file to <ip>:<port>
    @staticmethod
    def true_ip(line: str):
        ip, port = line.strip().split(':')
        return {'ip': ip, 'port': port}

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
    def calc(pings):
        p = [i for i in pings if isinstance(i, float)]
        send = len(pings)
        received = len(p)
        lost = send - received
        avg = minimum = maximum = None
        if p:  # if received:
            minimum = min(p)
            maximum = max(p)
            avg = sum(p) / len(p)
        print(f'Send:{send} / Received:{received} / Lost:{lost}')
        print(f'avg:{avg:.3} / min:{minimum:.3} / max:{maximum:.3}\n') if p else print('- OUT OF RANGE\n')
        return {'send': send, 'received': received, 'lost': lost, 'avg': avg, 'min': minimum, 'max': maximum}

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
        self.calc(pings)  # only presentation. no output
        return {'ip': ip, 'port': port, 'pings': pings, 'count': count}

    # ping ip s from list
    def list_ping(self, path):
        file = self.get_file(path)
        result = []
        for line in file:
            i = self.true_ip(line)
            result.append(self.get_ping(i['ip'], i['port'], self.count))
        return result

    # reset default values
    def wizard(self):
        self.ip = self.question('ip: ', '127.0.0.1')  # you can use 'self.ip' as answer
        self.port = self.question('port: ', 80)
        self.count = self.question('count number: ', 3)
        self.timeout = self.question('timeout', 3)

    # feature
    def validation(self):
        pass

    # help / manual
    def help(self):
        print(self.repr)
        for module in GetPing().__dir__():
            if not module.startswith('_'):
                n = f'GetPing().{module}'
                print(f'GetPing(). {module:10} \t | {type(eval(n))}')
