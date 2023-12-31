# Дипломный проект. Python backend разработчик.

### Описание
"Продуктовый помощник" - это сайт, на котором можно публиковать собственные рецепты, добавлять чужие рецепты в избранное, подписываться на других авторов и создавать список покупок для заданных блюд. Вот, что было сделано в ходе работы над проектом:
- настроено взаимодействие Python-приложения с внешними API-сервисами;
- создан собственный API-сервис на базе проекта Django;
- создан Telegram-бот;
- подключено SPA к бэкенду на Django через API;
- созданы образы и запущены контейнеры Docker;
- созданы, развёрнуты и запущены на сервере мультиконтейнерные приложения;
- закреплены на практике основы DevOps, включая CI&CD.

### Используемые технологии:
![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![image](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![image](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)
![image](https://img.shields.io/badge/VSCode-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)
![image](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)
![image](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![image](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![image](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

# Техническое задание
1. [Стек технологий](#Стек-технологий)
2. [Описание workflow](#Описание-workflow)
3. [Базовые модели проекта](#Базовые-модели-проекта)
4. [Главная страница](#Главная-страница)
5. [Страница рецепта](#Страница-рецепта)
6. [Страница пользователя](#Страница-пользователя)
7. [Подписка на авторов](#Подписка-на-авторов)
8. [Список избранного](#Список-избранного)
9. [Список покупок](#Список-покупок)
10. [Фильтрация по тегам](#Фильтрация-по-тегам)
11. [Регистрация и авторизация](#Регистрация-и-авторизация)
12. [Что могут делать неавторизованные пользователи](#Что-могут-делать-неавторизованные-пользователи)
13. [Что могут делать авторизованные пользователи](#Что-могут-делать-авторизованные-пользователи)
14. [Что может делать администратор](#Что-может-делать-администратор)
15. [Настройки админки](#Настройки-админки)
16. [Технические требования и инфраструктура](#Технические-требования-и-инфраструктура)
17. [Шаблон наполнения .env файла](#шаблон-наполнения-env-файла)

## Описание workflow
- Проверка кода на соответствие стандарту PEP8 с использованием пакета flake8.
- Сборка и доставка Docker-образа для контейнера web на Docker Hub.
- Автоматический деплой проекта на боевой сервер.

## Базовые модели проекта

### Рецепт - все поля обязательны для заполнения
- Автор публикации (пользователь)
- Название
- Картинка
- Текстовое описание
- Ингредиенты: продукты для приготовления блюда по рецепту. Множественное поле, выбор из предустановленного списка, с указанием количества и единицы измерения
- Тег (можно установить несколько тегов на один рецепт, выбор из предустановленных)
- Время приготовления в минутах

### Тег - все поля обязательны для заполнения и уникальны
- Название
- Цветовой HEX-код (например, #49B64E)
- Slug

### Ингредиент - все поля обязательны для заполнения
  Данные об ингредиентах хранятся в нескольких связанных таблицах. В результате на стороне пользователя ингредиент должен описываться такими полями:
- Название
- Количество
- Единицы измерения

## Главная страница
- Содержимое главной страницы — список первых шести рецептов, отсортированных по дате публикации (от новых к старым).
- Остальные рецепты доступны на следующих страницах: внизу страницы есть пагинация.

## Страница рецепта
- На странице — полное описание рецепта.
- Для авторизованных пользователей — возможность добавить рецепт в избранное и в список покупок, возможность подписаться на автора рецепта.

## Страница пользователя
- На странице — имя пользователя, все рецепты, опубликованные пользователем и возможность подписаться на пользователя.

[:arrow_up:Оглавление](#Оглавление)

## Подписка на авторов
- Подписка на публикации доступна только авторизованному пользователю.
- Страница подписок доступна только владельцу.
- Сценарий поведения пользователя:
  1. Пользователь переходит на страницу другого пользователя или на страницу рецепта и подписывается на публикации автора кликом по кнопке «Подписаться на автора».
  2. Пользователь переходит на страницу «Мои подписки» и просматривает список рецептов, опубликованных теми авторами, на которых он подписался. Сортировка записей — по дате публикации (от новых к старым).
  3. При необходимости пользователь может отказаться от подписки на автора: переходит на страницу автора или на страницу его рецепта и нажимает «Отписаться от автора».

## Список избранного
- Работа со списком избранного доступна только авторизованному пользователю.
- Список избранного может просматривать только его владелец.
- Сценарий поведения пользователя:
  1. Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в избранное».
  2. Пользователь переходит на страницу «Список избранного» и просматривает персональный список избранных рецептов.
  3. При необходимости пользователь может удалить рецепт из избранного.

## Список покупок
- Работа со списком покупок доступна авторизованным пользователям.
- Список покупок может просматривать только его владелец.
- Сценарий поведения пользователя:
  1. Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в покупки».
  2. Пользователь переходит на страницу Список покупок, там доступны все добавленные в список рецепты. Пользователь нажимает кнопку Скачать список и получает файл с суммированным перечнем и количеством необходимых ингредиентов для всех рецептов, сохранённых в «Списке покупок».
  3. При необходимости пользователь может удалить рецепт из списка покупок.
  - Список покупок скачивается в формате .txt (или, по желанию, можно сделать выгрузку PDF).
  - При скачивании списка покупок ингредиенты в результирующем списке не должны дублироваться; если в двух рецептах есть сахар (в одном рецепте 5 г, в другом — 10 г), то в списке должен быть один пункт: Сахар — 15 г.
  - В результате список покупок может выглядеть так:
    * Фарш (баранина и говядина) (г) — 600
    * Сыр плавленый (г) — 200
    * Лук репчатый (г) — 50
    * Картофель (г) — 1000
    * Молоко (мл) — 250
    * Яйцо куриное (шт) — 5
    * Соевый соус (ст. л.) — 8
    * Сахар (г) — 230
    * Растительное масло рафинированное (ст. л.) — 2
    * Соль (по вкусу) — 4
    * Перец черный (щепотка) — 3
## Фильтрация по тегам
При нажатии на название тега выводится список рецептов, отмеченных этим тегом. Фильтрация может проводиться по нескольким тегам в комбинации «или»: если выбраны несколько тегов — в результате должны быть показаны рецепты, которые отмечены хотя бы одним из этих тегов. При фильтрации на странице пользователя должны фильтроваться только рецепты выбранного пользователя. Такой же принцип должен соблюдаться при фильтрации списка избранного.

[:arrow_up:Оглавление](#Оглавление)

## Регистрация и авторизация
### Обязательные поля для пользователя
- Логин
- Пароль
- Email
- Имя
- Фамилия

### Уровни доступа пользователей
- Гость (неавторизованный пользователь)
- Авторизованный пользователь
- Администратор

## Что могут делать неавторизованные пользователи
- Создать аккаунт
- Просматривать рецепты на главной
- Просматривать отдельные страницы рецептов
- Просматривать страницы пользователей
- Фильтровать рецепты по тегам

## Что могут делать авторизованные пользователи
- Входить в систему под своим логином и паролем
- Выходить из системы (разлогиниваться)
- Менять свой пароль
- Создавать/редактировать/удалять собственные рецепты
- Просматривать рецепты на главной
- Просматривать страницы пользователей
- Просматривать отдельные страницы рецептов
- Фильтровать рецепты по тегам
- Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов
- Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл с количеством необходимых ингредиентов для рецептов из списка покупок
- Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок

## Что может делать администратор
Администратор обладает всеми правами авторизованного пользователя, а также может:
- Изменять пароль любого пользователя
- Создавать/блокировать/удалять аккаунты пользователей
- Редактировать/удалять любые рецепты
- Добавлять/удалять/редактировать ингредиенты
- Добавлять/удалять/редактировать теги

## Настройки админки
### Модели
- Вывести все модели с возможностью редактирования и удаления записей

### Модель пользователей:
- Добавить фильтр списка по email и имени пользователя

### Модель рецептов:
- В списке рецептов вывести название и автора рецепта
- Добавить фильтры по автору, названию рецепта, тегам
- На странице рецепта вывести общее число добавлений этого рецепта в избранное

### Модель ингредиентов:
- В список вывести название ингредиента и единицы измерения
- Добавить фильтр по названию

## Технические требования и инфраструктура
- Проект должен использовать базу данных PostgreSQL
- Код должен находиться в репозитории `foodgram-project-react`
- В Django-проекте должен быть файл `requirements.txt` со всеми зависимостями
- Проект нужно запустить в трёх контейнерах (nginx, PostgreSQL и Django) через docker-compose на вашем сервере в Яндекс.Облаке. Образ с проектом должен быть запушен на Docker Hub

## Шаблон наполнения .env файла

```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с PostgreSQL
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД
DB_HOST=db # хост базы данных
DB_PORT=5432 # порт для подключения к БД
SECRET_KEY='secret' # секретный ключ
ALLOWED_HOSTS='127.0.0.1,backend' # список разрешенных хостов
DEBUG=False # отключение режима отладки
```

## Инструкция по установке:

### Локальная установка:
1. Клонируйте репозиторий на компьютер:

```bash
   git@github.com:ocronis/foodgram-project-react.git
   cd foodgram-project-react

```

- Cоздать и активировать виртуальное окружение:

```bash
   python -m venv venv # Windows
```

```bash
   python3 -m venv venv # Linux
```

```bash
   source venv/Scripts/activate # Windows
```

```bash
   source venv/bin/activate # Linux
```

- Установить зависимости проекта:

```bash
   cd backend/foodgram/
```

```bash
   pip install -r requirements.txt
```

- Создать и выполнить миграции:

```bash
   python manage.py makemigrations
```

```bash
python manage.py migrate
```

- Запуск сервера локально:

```bash
   python manage.py runserver
```

- Создаём суперпользователя(admin/root):

```bash
   python manage.py createsuperuser
```

### **Запуск проекта на сервере в контейнерах:**

```
# МЕНЯЕМ БАЗУ SQLITE НА POSTGRES
pip install python-dotenv
# ИЗМЕНЯЕМ НАСТРОЙКИ БД В settings.pe
docker build -t ocronis/foodgram_frontend . # Собрали образ foodgram_frontend 
docker build -t ocronis/foodgram_backend . # Собрали образ foodgram_backend
docker push ocronis/foodgram_frontend # Запушили DockerHub
docker push ocronis/foodgram_backend # Запушили DockerHub
ssh ser@158.160.2.78 # Заходим на ВМ
Enter passphrase for key: # если Вы его установили
scp docker-compose.yml ser@158.160.2.78:/home/ser/docker-compose.yml
scp nginx.conf ser@158.160.2.78:/home/ser/nginx.conf
scp -r infra ser@158.160.2.78:/home/ser/infra # Копируем infra/ на сервер
sudo docker-compose up -d --build # создаём контейнеры
sudo docker-compose stop # останавливаем контейнеры
sudo docker-compose start # стартуем контейнеры
sudo docker-compose down -v # удаляем volumes
docker system prune --all --force # удаляем всё, если нам это необходимо
docker container ls -a # список контейнеров
docker image ls -a # список образов
sudo chmod 666 /var/run/docker.sock # хорошая команда
docker container rm # удаляем контейнер по ID
docker image rm # удаляем образ по ID
rm -r file_folder/ # удаляем необходимый файл
touch default.conf # создаём файл
nano docker-compose.yml # заходим в файл
ctrl + O # сохранить файл
Enter
ctrl + x # выйти из файла

# Для доступа к контейнеру backend и сборки финальной части выполняем следующие команды:
sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate --noinput
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --no-input
sudo docker-compose exec backend python manage.py importdata

# Отправляем на гит из нужной директории
git add .
git commit -m 'Final'
git push
```

### **Actions secrets**

```
DB_ENGINE
DB_HOST
DB_NAME
DB_PORT
DOCKER_PASSWORD
DOCKER_USERNAME
HOST
POSTGRES_PASSWORD
POSTGRES_USER
SECRET_KEY
SSH_KEY
TELEGRAM_TO
TELEGRAM_TOKEN
USER
```

### **Адрес сайта на Яндекс.Облаке:**
http://158.160.2.78:8000/signin Вход на сайт и регистрация <br>
http://158.160.2.78:8000/recipes Главная страница рецептов <br>
http://158.160.2.78:8000/subscriptions Подписки <br>
http://158.160.2.78:8000/recipes/create Создание рецепта <br>
http://158.160.2.78:8000/favorites Избранное <br>
http://158.160.2.78:8000/cart Список покупок <br>
---

### **Данные для входа в админку:**

```
Имя: Андрей
Фамилия: Сорокин
Имя пользователя: ocronis
Адрес электронной почты: sor@yan.ru
Пароль: 123456
```

Автор: [Сорокин Андрей](https://github.com/ocronis)
