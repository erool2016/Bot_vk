# VK BOT

## Бот предназначен для поиска знакмоств

### файл main.py имеет функции: 

users - принимает параметры поиска: access_token, city, sex, age_from, age_to. Выдает список 1000 пользвателей

info - принимает id клиента и список пользователей. Выдает одного пользвателя из списка и записывает в БД

send_some_msg - принимает id клиента и текст, для вывода. Выводит текст

send_info - принимает id клиента и список пользователей. Выводит одного пользователя

add_bl_user - принимает id клиента, добавляет в черный список

show_bl - принимает id клиента, выводит всех из ЧС

delete_bl - принимает id клиента и id пользователя, удаляет из ЧС

add_favorites_user - принимает id клиента, добавляет в избранные

show_fav - принимает id клиента, выводит всех из избранных

delete_fav - принимает id клиента и id пользователя, удаляет из избранных

main - принимает сообщения от клиента

### файл bd.py имеет функции:

add_users - принимает данные о пользователях user_id, first_name, last_name, href_us, bdate, sex, city, photos, записывает в БД

delete_users - принимает user_id, удаляет пользователей 

add_viewed_users - принимает user_id(клиент), user_id_view(пользователь), добавляет пользователей в просмотренные 

check_viewed_users - принимает user_id(клиент), выдает просмотренных

add_favorites - принимает user_id(клиент), user_id_fav(пользователь), добавляет пользователей в избранные

delete_favorites - принимает user_id(клиент), user_id_fav(пользователь), удаляет пользователей из избранных

show_favorites_id - принимает user_id(клиент), выдает user_id_fav(пользователь) избранных

show_favorites_info - принимает user_id_fav(пользователь), выдает инфо избранных

show_favorites_photos - принимает user_id_fav(пользователь), выдает фото избранных

add_black_list - принимает user_id(клиент), user_id_bd(пользователь), добавляет пользователей в ЧС

delete_black_list - принимает user_id(клиент), user_id_bd(пользователь), удаляет пользователей из ЧС

show_black_list_id - принимает user_id(клиент), выдает user_id_bd(пользователь) из ЧС

show_black_list_info - принимает user_id_bl(пользователь), выдает инфо из ЧС

show_black_list_photos - принимает user_id_bl(пользователь), выдает фото из ЧС

ckeck_users_add - принимает те же параметры, что и add_users, проверяет есть пользвоатель в БД, если нет, вызывает add_users

### файл bd.py:

Создает таблицы: Users, Viewed_users, Favorites, Black_list
