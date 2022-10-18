import time

import requests

val = 8
if __name__ == '__main__':
    val_s = str(val)
    requests.get(f'http://localhost:5000/ping/{val_s}')

    # while True:
    #     requests.get('http://localhost:5000/ping')
    #     time.sleep(1)
