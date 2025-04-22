# Образовательная Платформа

Django-приложение для управления образовательными курсами, лекциями, заданиями и оценками.

## Возможности

- Управление курсами (создание, обновление, удаление)
- Управление лекциями с версионированием контента
- Управление заданиями
- Управление вопросами с версионированием
- Управление ролями пользователей (студенты, модераторы, владельцы)
- Система отслеживания попыток и оценивания
- RESTful API для всех операций

## Требования

- Python 3.8 или выше
- PostgreSQL 12 или выше
- pip (менеджер пакетов Python)
- virtualenv (рекомендуется)

## Установка

### 1. Установка PostgreSQL на Linux

```bash
# Установка PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Запуск сервиса
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Создание пользователя и базы данных
sudo -u postgres psql

# В консоли PostgreSQL выполните:
CREATE DATABASE edu_app;
CREATE USER your_username WITH ENCRYPTED PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE edu_app TO your_username;
\q
```

### 2. Установка проекта

1. Клонируйте репозиторий:

```bash
git clone <url-репозитория>
cd edu_platform
```

2. Создайте и активируйте виртуальное окружение:

```bash
python -m venv venv
# В Windows
venv\Scripts\activate
# В Linux/Mac
source venv/bin/activate
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` в корневой директории проекта:

```bash
touch .env
```

5. Добавьте в файл `.env` следующие переменные:

```env
DB_NAME=edu_app
DB_USER=your_username
DB_USER_PASSWORD=your_password
```

6. Выполните миграции:

```bash
python manage.py migrate
```

7. Создайте суперпользователя:

```bash
python manage.py createsuperuser
```

8. Запустите сервер разработки:

```bash
python manage.py runserver
```

## Развертывание в продакшене

### 1. Настройка settings.py

1. Откройте файл `edu_platform/settings.py` и измените следующие настройки:
```python
DEBUG = False
ALLOWED_HOSTS = ['your_domain.com', 'www.your_domain.com']
CSRF_TRUSTED_ORIGINS = ['https://your_domain.com', 'https://www.your_domain.com']
```

### 2. Установка необходимых пакетов

```bash
# Установка Nginx
sudo apt update
sudo apt install nginx

# Установка Supervisor
sudo apt install supervisor
```

### 3. Настройка Gunicorn

1. Создайте файл конфигурации Gunicorn:

```bash
sudo nano /etc/supervisor/conf.d/edu_platform.conf
```

2. Добавьте следующую конфигурацию:

```ini
[program:edu_platform]
directory=/path/to/edu_platform
command=/path/to/edu_platform/venv/bin/gunicorn edu_platform.wsgi:application --workers 3 --bind 127.0.0.1:8000
autostart=true
autorestart=true
stderr_logfile=/var/log/edu_platform/err.log
stdout_logfile=/var/log/edu_platform/out.log
user=your_username
```

3. Создайте директорию для логов:

```bash
sudo mkdir /var/log/edu_platform
sudo chown your_username:your_username /var/log/edu_platform
```

4. Перезапустите Supervisor:

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start edu_platform
```

### 4. Настройка Nginx

1. Отредактируйте конфигурацию Nginx:

```bash
sudo nano /etc/nginx/sites-available/default
```

2. Замените содержимое на:

```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

3. Перезапустите Nginx:

```bash
sudo systemctl restart nginx
```

### 5. Проверка работоспособности

1. Проверьте статус Gunicorn:

```bash
sudo supervisorctl status edu_platform
```

2. Проверьте логи:

```bash
tail -f /var/log/edu_platform/out.log
tail -f /var/log/edu_platform/err.log
```

### 6. Полезные команды

```bash
# Перезапуск Gunicorn
sudo supervisorctl restart edu_platform

# Перезапуск Nginx
sudo systemctl restart nginx

# Просмотр логов Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Проверка статуса сервисов
sudo systemctl status nginx
sudo supervisorctl status
```

## Структура проекта

```
edu_platform/
├── courses/                 # Приложение управления курсами
│   ├── models.py           # Модели Course, Lecture, Task
│   ├── views.py            # API представления для курсов
│   └── urls.py             # Маршрутизация URL для курсов
├── assessments/            # Приложение управления оценками
│   ├── models.py           # Модели Question, Attempt
│   ├── views.py            # API представления для оценок
│   └── urls.py             # Маршрутизация URL для оценок
├── edu_platform/           # Основная директория проекта
│   ├── settings.py         # Настройки проекта
│   ├── urls.py             # Основная конфигурация URL
│   └── wsgi.py            # Конфигурация WSGI
└── requirements.txt        # Зависимости проекта
```

## Документация API

Платформа предоставляет RESTful API для всех операций. Вот основные категории эндпоинтов:

### Управление курсами

- `POST /course/create` - Создание нового курса
- `PUT /course/update` - Обновление деталей курса
- `POST /course/delete` - Удаление курса
- `POST /course/get` - Получение деталей курса

### Управление пользователями

- `POST /course/user/add` - Добавление пользователя в курс
- `POST /course/user/delete` - Удаление пользователя из курса
- `PUT /course/user/update` - Обновление роли пользователя

### Управление лекциями

- `POST /lecture/create` - Создание новой лекции
- `PUT /lecture/update` - Обновление содержимого лекции
- `POST /lecture/delete` - Удаление лекции
- `POST /lecture/get` - Получение деталей лекции

### Управление заданиями

- `POST /task/create` - Создание нового задания
- `PUT /task/update` - Обновление деталей задания
- `POST /task/get` - Получение деталей задания

### Управление вопросами

- `POST /question/create` - Создание нового вопроса
- `PUT /question/update` - Обновление содержимого вопроса
- `POST /question/get` - Получение деталей вопроса

### Управление попытками

- `POST /attempts/get` - Получение деталей попыток
- `POST /attempt/add` - Начало новой попытки
- `PUT /attempt/update` - Обновление попытки
- `POST /attempt/finish` - Завершение попытки
- `POST /attempt/grade` - Оценивание попытки

## Лицензия

Этот проект распространяется под лицензией MIT - подробности в файле LICENSE.
