from prometheus_client import start_http_server, Metric, REGISTRY
from threading import Lock
#from cachetools import cached, TTLCache
#from requests import Request, Session
#from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import argparse
import json
import logging
import os
import sys
import time

# lock of the collect method
lock = Lock()

# logging setup
log = logging.getLogger('export.cmc')
log.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s: %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


class CoinCollector():

  def collect(self):
    with lock:
      log.info('Fetching data')
      metric = Metric('rpi_temperature', 'motherboard temperature measurements', 'gauge')

      f = open("/sys/class/thermal/thermal_zone0/temp", "r")
      temp = f.read()
#      print('temp is ', temp)

      log.info('Received data')

      metric.add_sample('temperature_cpu', value=float(temp) / 1000.0, labels={})

      yield metric
      log.info('Data export complete')

      
if __name__ == '__main__':
  try:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--port', nargs='?', const=9102, help='The TCP port to listen on', default=9102)
    parser.add_argument('--addr', nargs='?', const='0.0.0.0', help='The interface to bind to', default='0.0.0.0')
    args = parser.parse_args()
    log.info('Listening on http://%s:%d/metrics' % (args.addr, args.port))

    REGISTRY.register(CoinCollector())
    start_http_server(int(args.port), addr=args.addr)

    while True:
      time.sleep(60)
  except KeyboardInterrupt:
    print(" Interrupted")
    exit(0)
