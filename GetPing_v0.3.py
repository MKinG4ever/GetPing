import time
import ping3
import random
import os
from platform import system
from sys import argv


class GetPing:
    """
        GetPing v0.3
        author: NightFox
        release: 7/10/2023
        see help as GetPing.help() for more information
    """

    def __init__(self):
        # Default IP/PORT
        self.ip = '127.0.0.1'  # default ip/port for monitoring mode feature (no effect on get_ping)
        self.port = '80'  # default port
        # Default value
        self.count = 5  # default count number (effect on list_ping)
        self.timeout = 3  # default timeout (effect on ping, get_ping, list_ping)
        self.version = 'GetPing v0.3'  # version information

    def __repr__(self):
        return f'{self.repr}ID:{id(self)}'  # rePresentation

    # Class presentation
    @property
    def repr(self):
        """portable presentation function"""
        return f'{self.version}\n{self.ip}[:{self.port}] \t (timeout={self.timeout} | count={self.count})\n'

    # simple time stamp
    @staticmethod
    def stamp():
        """time tracking function"""
        return time.time()

    # get/read the file
    @staticmethod
    def get_file(path):
        """simple file reader (with no limit)"""
        with open(path, 'r') as f:
            file = f.readlines()
        return file

    # interrupt function
    @staticmethod
    def delay(sec=None):
        """manual interrupt function to avoid bottleneck"""
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

    # validation test
    @staticmethod
    def validation(value, path='output'):
        """write strong pings/ip to file"""
        p = f'{path}.txt'
        v = value
        if v['received'] and v['max'] <= 1.5 and v['avg'] < 1:
            with open(p, 'a') as file:
                file.write(f'{v["ip"]}:{v["port"]}\n')

    # calculator function
    @staticmethod
    def calc(ip, port, pings, verbose=True):
        """advanced ping calculator function"""
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
        if verbose:
            print(f'Send:{send} / Received:{received} / Lost:{lost}')
            print(f'avg:{avg:.3} / min:{minimum:.3} / max:{maximum:.3}\n') if p else print('- OUT OF RANGE\n')
        return {'ip': ip, 'port': port, 'pings': pings, 'send': send, 'received': received, 'lost': lost,
                'avg': avg, 'min': minimum, 'max': maximum}

    # turn file to readable <ip>:<port> list
    def true_ip(self, path):
        """convert text-file to readable list for main function"""
        file = self.get_file(path)
        f = []
        for line in file:
            f.append(line.strip().split(':')) if ':' in line else f.append([line.strip(), ''])
        # f = [line.strip().split(':') for line in self.get_file(path)]
        return f

    # core function
    def ping(self, ip):
        """main ping function"""
        return ping3.ping(dest_addr=ip, timeout=self.timeout)  # set default timeout

    # main function
    def get_ping(self, ip, port='', count=1, verbose=True):
        """advanced ping function"""
        pings = []
        for _ in range(1, count + 1):
            print(f'[{_:3}] {ip}[:{port}] ... ', end='') if verbose else None
            p = self.ping(ip)
            pings.append(p)
            None if verbose is False else print(f'{p:.3}') if isinstance(p, float) else print(f'{p}')
        # pings = [self.ping(ip) for _ in range(count)]
        return self.calc(ip=ip, port=port, pings=pings, verbose=verbose)

    # ping ip s from list
    def list_ping(self, path, output=None):
        """advanced ping-list function"""
        file = self.true_ip(path)
        result = []
        for line in file:
            r = self.get_ping(ip=line[0], port=line[1], count=self.count)  # set default count number
            self.validation(value=r, path=output) if output else None
            result.append(r)
        # result = [self.get_ping(line[0], line[1], self.count) for line in file]
        return result

    # reset default values
    def wizard(self):
        """automate input process for all important values"""
        # you can use '<IP>' or 'self.ip' for answer.
        # Default IP/PORT
        self.ip = self.question('ip: ', '127.0.0.1')  # default ip/port for monitoring mode
        self.port = int(self.question('port: ', 80))
        # Default values
        self.count = int(self.question('count number: ', 5))
        self.timeout = int(self.question('timeout: ', 3))
        self.version = 'GetPing BetaVersion.'

    # help / manual
    def help(self):
        """make class more user-friendly with built-in help function"""
        print(self.repr)
        for module in GetPing().__dir__():
            if not module.startswith('_'):
                n = f'GetPing().{module}'
                print(f'GetPing().{module:10} \t | {type(eval(n))}')
        print('see github page for more.\n')
        print('- stamp() created.')
        print('- validation() updated.')
        print('- calc() upgraded.')
        print('- true_ip() upgraded.')
        print('- get_ping() upgraded.')
        print('- list_ping() upgraded.')
