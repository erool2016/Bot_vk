import sqlalchemy
from sqlalchemy.orm import sessionmaker
from bd.models_bd import Users, create_tables
from bd.models_bd import Favorites, Black_list, Viewed_users
import configparser


config = configparser.ConfigParser()
config.read('settings.ini')
login = config['ORM']['login']
password = config['ORM']['password']
name_bd = config['ORM']['name_bd']

DSN = f'postgresql://{login}:{password}@localhost:5432/{name_bd}'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_users(user_id: int, first_name: str, last_name: str, href_us, 
              bdate, sex: int, city: str, photos: str):
  '''добавление пользователей'''

  session.add(
    Users(
    user_id=user_id,
    first_name=first_name,
    last_name=last_name,
    href_us=href_us,
    bdate=bdate, 
    sex=sex,
    city=city,
    photos=photos
    )
  )
  session.commit()

def delete_users(user_id: int):
  '''удаление пользователей'''

  session.query(Users).filter(Users.user_id == user_id).delete()
  session.commit()

def add_viewed_users(user_id: int, user_id_view: int):
  '''добвление пользователей в просмотренные'''

  session.add(Viewed_users(user_id=user_id, user_id_view=user_id_view))
  session.commit()

def check_viewed_users(user_id: int):
  '''проверка просмотренных'''

  q = session.query(
  Viewed_users.user_id_view,
  ).filter(Viewed_users.user_id == user_id)

  return q

def add_favorites(user_id: int, user_id_fav: int):
  '''добавление пользователя в избранные'''

  session.add(Favorites(user_id=user_id, user_id_fav=user_id_fav))
  session.commit()

def delete_favorites(user_id: int, user_id_fav: int):
  '''удаление пользователя из избранных'''

  session.query(Favorites).filter(
    Favorites.user_id == user_id,
    Favorites.user_id_fav == user_id_fav
    ).delete()
  session.commit()

def show_favorites_id(user_id: int):
  '''вывод id избранных'''

  q = session.query(
    Users.user_id,
    ).join(
      Favorites.users_fav
      ).filter(Favorites.user_id == user_id)

  return q

def show_favorites_info(user_id_fav: int):
  '''вывод инфо об избранных'''

  q = session.query(
    Users.first_name,
    Users.last_name,
    Users.bdate,
    Users.sex,
    Users.city
    ).join(
      Favorites.users_fav
      ).filter(Favorites.user_id_fav == user_id_fav)

  return q

def show_favorites_photos(user_id_fav: int):
  '''вывод фото избр'''

  q = session.query(
    Users.photos
    ).join(
      Favorites.users_fav
      ).filter(Favorites.user_id_fav == user_id_fav)

  return q

def add_black_list(user_id: int, user_id_bl: int):
  '''добавление пользователя в черный список'''

  session.add(Black_list(user_id=user_id, user_id_bl=user_id_bl))
  session.commit()

def delete_black_list(user_id: int, user_id_bl: int):
  '''удаление пользователя из черного списка'''

  session.query(Black_list).filter(
    Black_list.user_id == user_id,
    Black_list.user_id_bl == user_id_bl
    ).delete()
  session.commit()

def show_black_list_id(user_id: int):
  '''вывод id пользователей в черном списке'''

  q = session.query(
  Users.user_id
  ).join(
    Black_list.users_bl
    ).filter(Black_list.user_id == user_id)

  return q

def show_black_list_info(user_id_bl: int):
  '''вывод инфо о пользователях в черном списке'''

  q = session.query(
  Users.first_name, 
  Users.last_name, 
  Users.bdate, 
  Users.sex, 
  Users.city
  ).join(
    Black_list.users_bl
    ).filter(Black_list.user_id_bl == user_id_bl)

  return q

def show_black_list_photos(user_id_bl: int):
  '''вывод фото пользователей в черном списке'''

  q = session.query(
  Users.photos
  ).join(
    Black_list.users_bl
    ).filter(Black_list.user_id_bl == user_id_bl)

  return q

def ckeck_users_add(
    user_id: int, 
    first_name: str, 
    last_name: str, 
    href_us: str, 
    bdate: str, 
    sex: int, 
    city: str, 
    photos: str
    ):
  '''проверка на то, есть ли пользователь уже в добавленных'''

  q = session.query(Users.user_id)
  list_us = []
  for i in q.all():
    for a in i:
      list_us.append(a)
  if user_id not in list_us:
    add_users(
      user_id, 
      first_name, 
      last_name, 
      href_us, 
      bdate, 
      sex, 
      city, 
      photos
      )

session.close()
