import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Users(Base):
  __tablename__ = "Users"

  id = sq.Column(sq.Integer, primary_key=True)
  user_id = sq.Column(sq.Integer, unique=True)
  first_name = sq.Column(sq.String(length=2000))
  last_name = sq.Column(sq.String(length=2000))
  href_us=sq.Column(sq.String(length=2000), unique=True)
  bdate = sq.Column(sq.String(length=2000))
  sex = sq.Column(sq.String(length=2000))
  city = sq.Column(sq.String(length=2000))
  photos = sq.Column(sq.String(length=2000), unique=True)

  def __str__(self):
    return (f'{self.id}, '
            f'{self.user_id}, '
            f'{self.first_name}, '
            f'{self.last_name}, '
            f'{self.href_us} '
            f'{self.bdate}, '
            f'{self.sex}, '
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
