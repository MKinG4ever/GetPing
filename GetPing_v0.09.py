import ping3


def main():
    """GetPing v0.09"""
    path = input('Enter file path: ')
    file = read_list('ip.txt')
    for line in file:
        i = get_ip(line)
        p = get_ping(i['ip'], i['port'], 3)
        print(p)
        if p['ping'] is not None and p['ping'] is not False:
            with open('online_servers.txt','a') as f:
                f.write(f'{p}\n')


def read_list(path):
    with open(path, 'r') as f:
        file = f.readlines()
    return file


def get_ip(value: str):
    ip, port = value.strip().split(':')
    return {'ip': ip, 'port': port}


def get_ping(ip, port, timeout):
    p = ping3.ping(dest_addr=ip, timeout=timeout)
    return {'ip': ip, 'port': port, 'ping': p}


if __name__ == '__main__':
    main()
