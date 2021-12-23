import requests
import json
import os
from datetime import *

from requests import HTTPError

from config import Config


def auth(url, credentials):
    headers = {"content-type": "application/json"}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(credentials))
        response.raise_for_status()
        return response.json()['access_token']

    except HTTPError:
        return None




def run(token, url, process_date, root_folder):

    os.makedirs(os.path.join(root_folder, process_date), exist_ok=True)

    headers = {"content-type": "application/json", "Authorization": "JWT " + token}

    try:
        response = requests.get(url, headers=headers, data=json.dumps({"date": process_date}))
        response.raise_for_status()

        with open(os.path.join(root_folder, process_date, 'result.json'), 'w') as json_file:
            response_data = response.json()
            json.dump(response_data, json_file)
            print('Date ' + process_date + ' successfully loaded')
    except HTTPError:
        print('Error for ' + process_date)


if __name__ == '__main__':

    config = Config(os.path.join('.', 'config.yaml'))

    url = config.get_config('url') + config.get_config('endpoint_auth')
    credentials = config.get_config('credentials')

    token = auth(url, credentials)

    if token is not None:

        url_data = config.get_config('url') + config.get_config('endpoint_data')
        payload_date = config.get_config('payload')
        current_date = datetime.strptime(payload_date['date'], '%Y-%m-%d')
        today = datetime.today()

        while current_date < today:
            run(token, url_data, current_date.strftime('%Y-%m-%d'), config.get_config('root_folder'))
            current_date = current_date + timedelta(days=1)

    else:
        print("Authentication is failed!")

