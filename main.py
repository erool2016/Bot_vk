import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from bd.bd import ckeck_users_add, add_viewed_users, check_viewed_users
from bd.bd import add_favorites, delete_favorites
from bd.bd import show_favorites_photos, show_favorites_info, show_favorites_id
from bd.bd import add_black_list, delete_black_list, show_black_list_photos
from bd.bd import show_black_list_id, show_black_list_info
import configparser


config = configparser.ConfigParser()
config.read('settings.ini')
key = config['ORM']['key']
access_token = config['ORM']['access_token']
vk_session = vk_api.VkApi(token=key)
session_api = vk_session.get_api()
longpool = VkLongPoll(vk_session)
count = -1
a_list = []

def users(
    access_token: str,
    city='',
    sex='',
    age_from='',
    age_to='',
    version='5.154'
    ):
  '''получает список пользователей'''

  global a_list
  url_1 = 'https://api.vk.com/method/users.search'
  params_1 = {
  'access_token': access_token,
  'count': 1000,
  'hometown': city,
  'sex': sex,
  'age_from': age_from,
  'age_to': age_to,
  'has_photo': 1,
  'v': version
  }

  response = requests.get(url_1, params={**params_1})
  a_list = response.json()['response']['items']

def info(us_id: int, users: list, version='5.154'):
  '''получает данные пользователя'''

  global count
  items = users[count]
  id = items['id']
  first_name = items['first_name']
  last_name = items['last_name']
  is_closed = items['is_closed']
  list_viev = []
  for id_vi in check_viewed_users(id):
    for id_v in id_vi:
      list_viev.append(id_v)
  if id not in list_viev:
    if is_closed != True:
      url_2 = 'https://api.vk.com/method/users.get'
      params_2 = {
      'access_token': access_token,
      'user_ids': id,
      'fields': 'bdate, city, sex, photo_max, domain',
      'v': version
      }
      response = requests.get(url_2, params={**params_2})
      short = response.json()['response'][0]
      href_us = 'https://vk.com/'+str(short['domain'])
      bdate = short['bdate']
      sex = short['sex']
      if 'city' in short.keys():
        city = short['city']['title']
      else:
        city = 'город не указан'
      url_3 = 'https://api.vk.com/method/photos.get'
      params_3 = {
        'access_token': access_token,
        'owner_id': id,
        'album_id': 'profile',
        'rev': '1',
        'extended': '1',
        'v': '5.154'
        }
      response = requests.get(url_3, params={**params_3})
      data = response.json()['response']['items']
      if response.json()['response']['count'] > 3:
        list_href = []
        dict_likes = {}
        list_href_top_3 = []
        for ph in data:
          dict_likes[ph['likes']['count']] = ph['id']
        sort_list_likes = dict(sorted(dict_likes.items()))
        for like in sort_list_likes:
          list_href.append(sort_list_likes[like])
        list_href_top_3.append(list_href[-1])
        list_href_top_3.append(list_href[-2])
        list_href_top_3.append(list_href[-3])
        list_id_ph = []
        for ph_id in list_href_top_3:
          list_id_ph.append(f'photo{id}_{ph_id}_{key}')
        str_list_id_ph = ' '.join(list_id_ph)
        ckeck_users_add(
          id,
          first_name,
          last_name,
          href_us,
          bdate,
          sex,
          city,
          str_list_id_ph,
          )
        list_123 = []
        list_123.append(id)
        list_123.append(first_name)
        list_123.append(last_name)
        list_123.append(href_us)
        list_123.append(list_id_ph)
        add_viewed_users(us_id, id)
        return list_123
      else:
        count += 1
        send_info(us_id, a_list)
    else:
      count += 1
      send_info(us_id, a_list)
  else:
    count += 1
    send_info(us_id, a_list)

def send_some_msg(id: int, some_text: str):
  '''выдает отбивку пользователю'''

  vk_session.method(
    "messages.send",
    {
      "user_id":id,
      "message":some_text,
      "random_id":0
      }
      )

def send_info(id: int, users: list):
  '''отправляет информацию o пользователе'''

  us_inf = info(id, users)
  if type(us_inf) == str:
    answer = us_inf
    vk_session.method(
      "messages.send",
      {
        "user_id":id,
        "message":answer,
        "random_id":0,
        }
        )
  elif type(us_inf) == list:
    answer = f'{us_inf[1]} {us_inf[2]}\n{us_inf[3]}'
    vk_session.method(
      "messages.send",
      {
        "user_id":id,
        "message":answer,
        "random_id":0,
        }
        )
    for ph in us_inf[-1]:
      vk_session.method(
        "messages.send",
        {
          "user_id":id,
          "attachment":ph,
          "random_id":0,
          }
          )

def add_bl_user(id: int):
  '''добавление в черный список'''

  global a_list
  global count
  items = a_list[count]
  id_b = items['id']
  add_black_list(id, id_b)
  send_some_msg(id, 'добавлено')

def show_bl(id: int):
  '''вывод из ЧС'''

  for i in show_black_list_id(id):
    for a in i:
      send_some_msg(id, f'id пользователя: {a}')
      str_info = ''
      for b in show_black_list_info(a):
        for u in b:
          str_info += f'{u}\n'
      send_some_msg(id, str_info)
      for v in show_black_list_photos(a):
        for h in v:
          l_p = h.split(' ')
          for p in l_p:
            vk_session.method(
              "messages.send", 
              {
                "user_id":id, 
                "attachment":p,
                "random_id":0,
                }
                )

def delete_bl(id: int, id_fav: int):
  '''удаление из ЧС'''

  delete_black_list(id, id_fav)

def add_favorites_user(id: int):
  '''добавление в избранное'''

  global a_list
  global count
  items = a_list[count]
  id_f = items['id']
  add_favorites(id, id_f)
  send_some_msg(id, 'добавлено')

def show_fav(id: int):
  '''вывод избранных'''

  for i in show_favorites_id(id):
    for a in i:
      send_some_msg(id, f'id пользователя: {a}')
      str_info = ''
      for b in show_favorites_info(a):
        for u in b:
          str_info += f'{u}\n'
      send_some_msg(id, str_info)
      for v in show_favorites_photos(a):
        for h in v:
          l_p = h.split(' ')
          for p in l_p:
            vk_session.method(
              "messages.send", 
              {
                "user_id":id, 
                "attachment":p,
                "random_id":0,
                }
                )

def delete_fav(id: int, id_fav: int):
  '''удаление из избранных'''
  delete_favorites(id, id_fav)

par = []

def main():
  '''main'''

  global count
  global a_list
  global par

  for event in longpool.listen():
    if event.type == VkEventType.MESSAGE_NEW:
      if event.to_me:
        msg = event.text.lower()
        id = event.user_id
        if msg == 'начать':
          send_some_msg(
            id,
            'Чтобы выбрать город, введите "city:город"\n'
            'Чтобы выбрать какого пола искать людей, введите "sex:цифра", '
            'где 1 - это Ж, 2 - M, 0 - не указан\n'
            'Чтобы выбрать от какого возраста искать, '
            'введите "age_from:число"\n'
            'Чтобы выбрать до какого возраста искать, введите "age_to:число"\n'
            'Чтобы добавить в избранное, введите "add_fav"\n'
            'Чтобы показать избранных, введите "show_fav"\n'
            'Чтобы удалить из избранных, введите "del_fav:id человека"\n'
            'Чтобы добавить в ЧС, введите "add_bl"\n'
            'Чтобы показать ЧС, введите "show_bl"\n'
            'Чтобы удалить из ЧС, введите "del_bl:id человека"\n'
            )
          url_add = 'https://api.vk.com/method/users.get'
          params_add = {
          'access_token': access_token,
          'user_ids': id,
          'fields': 'bdate, city, sex, photo_max, domain',
          'v': '5.154'
          }
          response = requests.get(url_add, params={**params_add})
          data = response.json()['response'][0]
          short_href = response.json()['response'][0]['domain']
          href_us = 'https://vk.com/'+short_href
          id = data['id']
          sex = data['sex']
          first_name = data['first_name']
          last_name = data['last_name']
          bdate = data['bdate']
          if 'city' in data.keys():
            city = data['city']['title']
          else:
            city = 'город не указан'
          photo_max = data['photo_max']
          ckeck_users_add(
            id,
            first_name,
            last_name,
            href_us,
            bdate,
            sex,
            city,
            photo_max
            )
        if 'city' in msg:
          city = msg.split(':')[1]
          par.append(city)
          send_some_msg(id, 'принято')
        if 'sex' in msg:
          sex = msg.split(':')[1]
          par.append(sex)
          send_some_msg(id, 'принято')
        if 'age_from' in msg:
          age_from = msg.split(':')[1]
          par.append(age_from)
          send_some_msg(id, 'принято')
        if 'age_to' in msg:
          age_to = msg.split(':')[1]
          par.append(age_to)
          send_some_msg(id, 'введите "дальше", чтобы перейти к найти кого-то')
        if a_list == [] and len(par) > 3:
          users(access_token, city, sex, age_from, age_to)
        if msg == 'дальше':
          count += 1
          send_info(id, a_list)
        if msg == 'add_fav':
          add_favorites_user(id)
        if msg == 'show_fav':
          show_fav(id)
        if 'del_fav' in msg:
          us_fav = msg.split(':')[1]
          delete_fav(id, us_fav)
          send_some_msg(id, 'удалено')
        if msg == 'add_bl':
          add_bl_user(id)
        if msg == 'show_bl':
          show_bl(id)
        if 'del_bl' in msg:
          us_fav = msg.split(':')[1]
          delete_bl(id, us_fav)
          send_some_msg(id, 'удалено')
