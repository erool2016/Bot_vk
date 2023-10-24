import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Users(Base):
  __tablename__ = "Users"

  id = sq.Column(sq.Integer, primary_key=True)
  user_id = sq.Column(sq.Integer, unique=True)
  name = sq.Column(sq.String(length=40))
  surname = sq.Column(sq.String(length=40))
  age = sq.Column(sq.Integer)
  gender = sq.Column(sq.String(length=20))
  city = sq.Column(sq.String(length=40))
  photos = sq.Column(sq.String(length=300), unique=True)

  def __str__(self):
    return (f'{self.id}, '
            f'{self.user_id}, '
            f'{self.name}, '
            f'{self.surname}, '
            f'{self.age}, '
            f'{self.gender}, '
            f'{self.city}, '
            f'{self.photos}')

class Viewed_users(Base):
  __tablename__ = "Viewed_users"

  id = sq.Column(sq.Integer, primary_key=True)
  user_id = sq.Column(sq.Integer)
  user_id_view = sq.Column(sq.Integer, sq.ForeignKey("Users.user_id"))

  users_view = relationship(Users, backref='Viewed_users')

  def __str__(self):
    return f'{self.user_id}, {self.user_id_view}'

class Favorites(Base):
  __tablename__ = "Favorites"

  id = sq.Column(sq.Integer, primary_key=True)
  user_id = sq.Column(sq.Integer)
  user_id_fav = sq.Column(sq.Integer, sq.ForeignKey("Users.user_id"))

  users_fav = relationship(Users, backref='Favorites')

  def __str__(self):
    return f'{self.user_id}, {self.user_id_fav}'

class Black_list(Base):
  __tablename__ = "Black_list"

  id = sq.Column(sq.Integer, primary_key=True)
  user_id = sq.Column(sq.Integer)
  user_id_bl = sq.Column(sq.Integer, sq.ForeignKey("Users.user_id"), nullable=False)

  users_bl = relationship(Users, backref='Black_list')

  def __str__(self):
    return f'{self.user_id}, {self.user_id_bl}'

def create_tables(engine):
  Base.metadata.drop_all(engine) # удаление таблиц
  Base.metadata.create_all(engine) # создание таблиц
