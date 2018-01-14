import atexit
import json
import os
import sys
import time
from requests_threads import AsyncSession
sys.path.append('./')
import coins
import database

def daemonize(pid_file=None):
    pid = os.fork()
    if pid:
        sys.exit(0)
    os.chdir('/')
    os.umask(0)
    os.setsid()
    _pid = os.fork() # Fork again, the grandson process is daemon process now.
    if _pid:
        sys.exit(0)
    sys.stdout.flush()
    sys.stderr.flush()
    # Close read/write
    with open('/dev/null') as read_null, open('/dev/null', 'w') as write_null:
        os.dup2(read_null.fileno(), sys.stdin.fileno())
        os.dup2(write_null.fileno(), sys.stdout.fileno())
        os.dup2(write_null.fileno(), sys.stderr.fileno())
    if pid_file:
        with open(pid_file, 'w+') as f:
            f.write(str(os.getpid()))
        # Register exit function to remove pid file
        atexit.register(os.remove, pid_file)
    # Do works
    session = AsyncSession(n=(os.cpu_count() * 2))
    fetch_ticker.session = session
    session.run(fetch_ticker)
    
def write_tops(prices):
    data = []
    for item in prices:
        data.append('%s:%.09f' % (item['code'], item['price']))
    r = database.btc_tops()
    r.data = '\n'.join(data)
    r.save()

def write_bottoms(prices):
    data = []
    for item in prices:
        data.append('%s:%.09f' % (item['code'], item['price']))
    r = database.btc_bottoms()
    r.data = '\n'.join(data)
    r.save()

async def fetch_ticker():
    session = fetch_ticker.session
    while True:
        responses = []
        for coin in coins.coins:
            responses.append(await session.get('https://www.okex.com/api/v1/ticker.do?symbol=%s_btc' % coin))
        prices = []
        for resp in responses:
            jdata = resp.json()
            url = resp.url
            code = url.split('?')[1].split('=')[1].split('_')[0]
            price = float(jdata['ticker']['last'])
            prices.append({'code': code, 'price': price})
            r = database.btc_values()
            r.code = code
            r.price = price
            r.save()
        prices = sorted(prices, key=lambda x: x['price'])
        write_tops(prices[-6:-1][::-1])
        write_bottoms(prices[:5])
        time.sleep(30)

def write_btc_kdata(prices, tag):
    data = []
    for item in prices:
        data.append('%s: %.09f, %.03f' % (item['code'], item['close'], item['pct_change']))
    r = database.btc_bottoms()
    r.data = '\n'.join(data)
    r.tag = tag
    r.save()

async def fetch_kline():
    session = fetch_kline.session
    ks = ['15min', '1hour', '1day']
    while True:
        for k in ks:
            responses = []
            for coin in coins.coins:
                responses.append(await session.get('https://www.okex.com/api/v1/kline.do?symbol=%s&type=%s&size=1' % \
                                                   (coin, k)))
            k_datas = []
            for response in responses:
                jdata = response.json()[0] # Becasue it returns an array of arrays
                url = resp.url
                code = url.split('?')[1].split('&')[0].split('=')[1]
                open_ = jdata[1]
                close_ = jdata[4]
                pct_change = (close_ - open_) / open_ # all day trading...
                k_datas.append({'code': code,
                                'open': open_,
                                'close': close_,
                                'pct_change': pct_change})
            k_datas = sorted(k_datas, key=lambda x: x['pct_change'])
            top5 = k_data[-6:-1][::-1]
            bottom5 = k_data[:5]
            write_btc_kdata(top5, 'top5_%s' % k)
            write_btc_kdata(bottom5, 'bottom5_%s' % k)          

if __name__ == '__main__':
    # Hard code the file path because we'll set the dir to root
    daemonize('/home/bear/work/github/bithelper/okex_data/pid.txt')
