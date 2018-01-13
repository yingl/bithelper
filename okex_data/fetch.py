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
    while True:
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
    print('sleep 15s...')
    time.sleep(15)

if __name__ == '__main__':
    """
    session = AsyncSession(n=(os.cpu_count() * 2))
    while True:
        session.run(fetch_ticker)
    """
    daemonize('pid.txt')
