import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Users(Base):
  __tablename__ = "Users"

  id = sq.Column(sq.Integer, primary_key=True)
  user_id = sq.Column(sq.Integer, unique=True)
  name = sq.Column(sq.String(length=40))
  surname = sq.Column(sq.String(length=40))
  age = sq.Column(sq.String(length=3))
  gender = sq.Column(sq.String(length=20))
  city = sq.Column(sq.String(length=40))
  photos = sq.Column(sq.String(length=300), unique=True)

  def __str__(self):
    return f'{self.id}, {self.user_id}, {self.name}, {self.surname}, {self.age}, {self.gender}, {self.city}, {self.photos}'


class Favorites(Base):
  __tablename__ = "Favorites"

  id = sq.Column(sq.Integer, primary_key=True)
  user_id = sq.Column(sq.Integer, sq.ForeignKey("Users.id"), nullable=False)
  user_id_fav = sq.Column(sq.Integer, sq.ForeignKey("Users.id"), nullable=False)

  users_fav = relationship(Users, backref="Favorites")


class Black_list(Base):
  __tablename__ = "Black_list"

  id = sq.Column(sq.Integer, primary_key=True)
  user_id = sq.Column(sq.Integer, sq.ForeignKey("Users.id"), nullable=False)
  user_id_bl = sq.Column(sq.Integer, sq.ForeignKey("Users.id"), nullable=False)

  users_bl = relationship(Users, backref="Black_list")


def create_tables(engine):
  # Base.metadata.drop_all(engine) # удаление таблиц
  Base.metadata.create_all(engine) # создание таблиц
