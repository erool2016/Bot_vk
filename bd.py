import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models_bd import Users, create_tables
from models_bd import Favorites, Black_list, Viewed_users
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

def add_users(user_id: int, name: str, surname: str, 
              age: int, gender: str, city: str, photos: str):
  '''добавление пользователей'''

  session.add(
    Users(
    user_id=user_id,
    name=name,
    surname=surname,
    age=age, gender=gender,
    city=city,
    photos=photos
    )
  )
  session.commit()

def delete_users(user_id: int):
  '''удаление пользователей'''

  session.query(Users).filter(Users.user_id == user_id).delete()
  session.commit()

def show_users(user_id: int, age_low: int, age_high: int, gender: str,
               city: str):
  '''вывод пользователей по критериям'''

  q = session.query(
    Users.name,
    Users.surname,
    Users.age,
    Users.gender,
    Users.city,
    Users.photos
    ).filter(
      Users.user_id == user_id,
      Users.age >= age_low,
      Users.age <= age_high,
      Users.gender == gender,
      Users.city == city
      )

  return q

def add_viewed_users(user_id: int, user_id_view: int):
  '''добвление пользователей в просмотренные'''

  session.add(Viewed_users(user_id=user_id, user_id_view=user_id_view))
  session.commit()

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

def show_favorites(user_id: int):
  '''вывод избранных'''

  q = session.query(
    Users.name, 
    Users.surname, 
    Users.age, 
    Users.gender, 
    Users.city, 
    Users.photos
    ).join(
      Favorites.users_fav
      ).filter(Favorites.user_id == user_id)

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

def show_black_list(user_id: int):
  '''вывод пользователей в черном списке'''

  q = session.query(
  Users.name, 
  Users.surname, 
  Users.age, 
  Users.gender, 
  Users.city, 
  Users.photos
  ).join(
    Black_list.users_bl
    ).filter(Black_list.user_id == user_id)

  return q

# def check_users(user_id: int, age_low: int, age_high: int, gender: str,
#               city: str):
#   '''выводит всех, кроме просмотренных, избранных, чс и себя'''

#   list_us = []
#   exceptions = []

#   q_viewed_users = session.query(Viewed_users.user_id_view).filter(
#     Viewed_users.user_id == user_id
#    )
#   q_favorites = session.query(Favorites.user_id_fav).filter(
#     Favorites.user_id == user_id
#    )
#   q_black_list = session.query(Black_list.user_id_bl).filter(
#     Black_list.user_id == user_id
#    )
#   q_users = session.query(Users.user_id).all()

#   list_users_ex = [q_viewed_users, q_favorites, q_black_list]

#   for q in list_users_ex:
#     for q_1 in q.all():
#       for q_2 in q_1:
#         exceptions.append(q_2)

#   for q in q_users:
#     for q_1 in q:
#       list_us.append(q_1)

#   show_list = [x for x in list_us if x not in exceptions]

#   for id in show_list:
#     if id != user_id:
#       for user in show_users(id, age_low, age_high, gender, city):
#         return user

def check_users_view(user_id: int):
  '''проверяет, есть ли user_id в просмотренных'''

  q_viewed_users = session.query(Viewed_users.user_id_view).filter(
    Viewed_users.user_id_view == user_id
  ).all()

  return bool(q_viewed_users)

session.close()
