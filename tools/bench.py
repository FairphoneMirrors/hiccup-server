import json, requests
from multiprocessing import Pool

clients = []


BASE_URL = 'http://127.0.0.1:8000/hiccup/'

def create_client():
    ret_client = {}
    register_url = 'api/v1/devices/register/'
    params =  {
        'board_date': "2017-01-01",
        'chipset': "HICCUPBENCH"
    }
    resp = requests.post(BASE_URL+register_url, params)
    data = json.loads(resp.text)
    ret_client['token'] = data['token']
    ret_client['uuid'] = data['uuid']
    return ret_client


def send_heartbeat(client):
    heartbeat_url = 'api/v1/heartbeats/'
    params = {
        'uuid': client['uuid'],
        'build_fingerprint': 'HICCUPBENCH',
        'uptime': "string",
        'date': "1984-06-02T19:05:00.000Z",
        'app_version' : 2000000
    }
    resp = requests.post(BASE_URL + heartbeat_url, params,
            headers = {'Authorization': 'Token '+ client['token']})
    return resp

import time

def bench(client):
    start_time = time.time()
    for i in range(50):
        send_heartbeat(client)
    end_time = time.time()
    print(end_time-start_time)

clients = []
for  i in range(20):
    clients =  clients + [create_client()]

with Pool(20) as p:
    p.map(bench, clients)
