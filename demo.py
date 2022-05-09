# 深信服 WebVPN 内网存活网站探测 Demo

from IPy import IP
import argparse
import requests
from concurrent.futures import ThreadPoolExecutor, wait

requests.packages.urllib3.disable_warnings()

headers = {
    'Cookie': 'xxxxxx',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
}


# portlist = [
#     80, 8080, 81, 8081, 7001, 8000, 8088, 8888, 9090, 8090, 88, 8001, 82, 9080, 8082, 8089, 9000, 8443, 9999, 8002,
#     89, 8083, 8200, 90, 8086, 801, 8011, 8085, 9001, 9200, 8100, 8012, 85, 8084, 8070, 8091, 8003, 7777, 8010, 443,
#     8028, 8087, 83, 10000, 8181, 8099, 8899, 8360, 8300, 9002, 8053, 1000, 8989, 9060, 888, 8006, 6677, 7200, 8280,
#     8161, 8880, 8020, 7070, 889, 1010, 8004, 86, 38501, 41516, 28017, 18080, 7002, 808, 800, 8099, 8800, 8180,
#     3505, 7080, 8484, 9003
# ]


def iplist(ips):
    urllist = []
    iplist = IP(ips)
    for ip in iplist[1:-1]:
        # for port in portlist:
        #     urllist.append(str(ip).replace('.', '-', 3) + '-' + str(port))
        urllist.append(str(ip).replace('.', '-', 3))
    return urllist


def exploit(ip):
    url = f'http://{ip}.sangfor.vpn.x.x.x'
    print(f'[*] 正在访问 {url}')
    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        if response.status_code != 502:
            print(f'[+] 连接存活 {url}')
            result(url)
    except:
        pass


def result(target):
    file = open('re.txt', 'a')
    file.write(target + '\n')
    file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='demo')
    parser.add_argument('-i', '--ips', help='目标 IP 段')
    parser.add_argument('-t', '--threads', default=100, help='设置线程数 默认 100')
    args = parser.parse_args()
    if args.ips:
        ips = iplist(args.ips)
        poolList = []
        pool = ThreadPoolExecutor(max_workers=int(args.threads))
        for ip in ips:
            poolList.append(pool.submit(lambda p: exploit(*p), [ip]))
        wait(poolList)
