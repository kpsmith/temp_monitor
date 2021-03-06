from client.wemo import WemoClient
from client.dynamo import DynamoClient
from client.dynamostream import DynamoStreamClient
import time
import util
import Queue

def main():
    try:
        print('controlling wemo')
        control_wemo()
    except Exception:
        time.sleep(10)
        main()

def control_wemo():
  wc = WemoClient()
  dc = DynamoClient('miscellaneous')
  queue = Queue.Queue()
  queue_list = [queue]
  old_items = []
  dsc = DynamoStreamClient(queue_list, old_items, util.temp_hist_arn)
  dsc.start()
  try:
      while True:
        d = queue.get()
        max_temp = dc.get_max_temp()
        min_temp = dc.get_min_temp()
        temp = d['temperature']
        if temp > max_temp:
          wc.switch_off()
        elif temp < min_temp:
          wc.switch_on()
  finally:
    dsc.stop()

if __name__ == '__main__':
    main()
