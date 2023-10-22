import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models_bd import Users, create_tables
from models_bd import Favorites, Black_list
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

def show_users(age_low: int, age_high: int, gender: str,
               city: str, photos: str):
  '''вывод пользователей по критериям'''

  q = session.query(Users).filter(
    (age_low <= Users.age <= age_high),
    Users.gender == gender,
    Users.city == city,
    Users.photos == photos
    )

  return q.all()

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
      ).filter(
        user_id == user_id
        )
  
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
    ).filter(
      user_id == user_id
      )

  return q.all()

session.close()
