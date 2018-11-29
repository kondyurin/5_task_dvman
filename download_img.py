import os
import requests
from dotenv import load_dotenv


load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


def fetch_json(url, params):
    response = requests.get(url,params)
    data = response.json()
    return data


def load_img(url):
    filename = 'python.png'
    response = requests.get(url)
    with open(filename, 'wb') as f:  
        f.write(response.content)


def get_server_address():
    payload = {
    'group_id': 174503727,
    'v': '5.92',
    'access_token': ACCESS_TOKEN
    }
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    result = fetch_json(url, params=payload)
    return result


def send_img(url):
    files = {'file1': open('python.png', 'rb')}
    response = requests.post(url, files=files)
    data = response.json()
    print(type(data))
    return data


def save_img(data):
    server = data['server']
    photo = data['photo']
    hash_ = data['hash']
    print(type(photo))
    payload = {
    'photo': photo,
    'server': server,
    'hash': hash_,
    'access_token': ACCESS_TOKEN,
    'v': '5.92'
    }
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    result = fetch_json(url, params=payload)
    return result
    

def main():
    pass


server_address = get_server_address()['response']['upload_url']
res_json = save_img(send_img(server_address))
print(res_json)
