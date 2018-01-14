import argparse
import os
import sys
import time
sys.path.append('./')
import coins
import util

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d',
                        '--debug',
                        type=bool,
                        default=False)
    return parser.parse_args()

def write_to_aggs(prices, tag):
    data = []
    for item in prices:
        data.append('%s:%.09f' % (item['code'], item['price']))
    util.write_aggs('\n'.join(data), tag)

async def fetch_ticker():
    session = fetch_ticker.session
    while True:
        responses = []
        for coin in coins.coins:
            responses.append(await session.get('https://www.okex.com/api/v1/ticker.do?symbol=%s_btc' % coin))
        prices = []
        for response in responses:
            jdata = response.json()
            url = response.url
            code = url.split('?')[1].split('=')[1].split('_')[0]
            price = float(jdata['ticker']['last'])
            prices.append({'code': code, 'price': price})
            util.write_values(code, price)
        prices = sorted(prices, key=lambda x: x['price'])
        write_to_aggs(prices[-6:-1][::-1], 'bts_price_top5')
        write_to_aggs(prices[:5], 'bts_price_bottom5')
        time.sleep(45)

if __name__ == '__main__':
    args = parse_args()
    util.daemonize(fetch_ticker,
                   os.path.join(os.getcwd(), 'pid_ticker.txt'),
                   args.debug)
