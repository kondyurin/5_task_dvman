import os
import requests
from dotenv import load_dotenv
from random import randint


load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


def fetch_json(url, params):
    response = requests.get(url,params)
    data = response.json()
    return data


def get_random_comics():
    url = 'http://xkcd.com/info.0.json'
    response = requests.get(url)
    data = response.json()
    last_num = data['num']
    random_comics = randint(1, last_num)
    return random_comics


def load_img():
    random_comics = get_random_comics()
    url = 'https://xkcd.com/{}/info.0.json'.format(random_comics)
    print(url)
    response = requests.get(url)
    data = response.json()
    img_url = data['img']
    filename = '{}.png'.format(random_comics)
    print(filename)
    response = requests.get(img_url)
    with open(filename, 'wb') as f:  
        f.write(response.content)
    return data, filename


def get_server_address():
    payload = {
    'group_id': 174503727,
    'v': '5.92',
    'access_token': ACCESS_TOKEN
    }
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    result = fetch_json(url, params=payload)
    return result


def send_img(url, filename):
    files = {'file1': open(filename, 'rb')}
    response = requests.post(url, files=files)
    os.remove(filename)
    data = response.json()
    return data


def save_img(data):
    server = data['server']
    photo = data['photo']
    hash_ = data['hash']
    payload = {
    'photo': photo,
    'server': server,
    'hash': hash_,
    'access_token': ACCESS_TOKEN,
    'v': '5.92',
    'group_id': 174503727
    }
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    result = fetch_json(url, params=payload)
    return result


def wall_post(result, data):
    owner_id_main = -174503727
    owner_id = result['response'][0]['owner_id']
    media_id = result['response'][0]['id']
    message = data['title']
    attachments = 'photo{}_{}'.format(owner_id, media_id)
    payload = {
    'owner_id': owner_id_main,
    'from_group': 1,
    'access_token': ACCESS_TOKEN,
    'attachments': attachments,
    'v': '5.92',
    'group_id': 174503727,
    'message': message
    }
    url = 'https://api.vk.com/method/wall.post'
    result = fetch_json(url, params=payload)
    return result


def main():
    data, filename = load_img()
    server_address = get_server_address()['response']['upload_url']
    res_json = wall_post(save_img(send_img(server_address, filename)), data)
    print(res_json, filename)


if __name__ == '__main__':
    main()


