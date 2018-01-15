import argparse
import logging
import os
import sys
import time
import traceback
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
        print(item)
        data.append('%s: %.09f, %.02f%%' % (item['code'], item['close'], item['pct_chg']))
    util.write_aggs('\n'.join(data), tag)

async def fetch_kline():
    logging.basicConfig(filename=fetch_kline.log_file, level=logging.INFO)
    session = fetch_kline.session
    ks = ['15min', '1hour']
    while True:
        try:
            for k in ks:
                responses = []
                for coin in coins.coins:
                    url = 'https://www.okex.com/api/v1/kline.do?symbol=%s_btc&type=%s&size=1' % \
                          (coin, k)
                    responses.append(await session.get(url)) 
                prices = []
                for response in responses:
                    jdata = response.json()[0] # Becasue it returns an array of arrays
                    url = response.url
                    code = url.split('?')[1].split('&')[0].split('=')[1].split('_')[0]
                    open_ = float(jdata[1])
                    close_ = float(jdata[4])
                    pct_chg = (close_ - open_) / open_ * 100.0 # all day trading...
                    prices.append({'code': code,
                                   'open': open_,
                                   'close': close_,
                                   'pct_chg': pct_chg})
                prices = sorted(prices, key=lambda x: x['pct_chg'])
                write_to_aggs(prices[-6:-1][::-1], 'bts_change_%s_top5' % k)
                write_to_aggs(prices[:5], 'bts_change_%s_bottom5' % k)
        except Exception as e:
            logging.error(e)
            logging.error(traceback.format_exc())
        time.sleep(60)

if __name__ == '__main__':
    args = parse_args()
    util.daemonize(fetch_kline,
                   os.path.join(os.getcwd(), 'pid_kline.txt'),
                   args.debug)
