# Home — магазин мебели

Учебный Django-проект: каталог товаров, поиск, корзина, регистрация, профиль и оформление заказов.

## Локальный запуск в Windows

Нужны Python 3.14 и PostgreSQL. Создайте пустую базу PostgreSQL и пользователя с доступом к ней.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Заполните `.env`: имя базы, пользователя, пароль и новый `DJANGO_SECRET_KEY`. Создать ключ можно так:

```powershell
.\.venv\Scripts\python.exe -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Затем выполните:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

Откройте http://127.0.0.1:8000/ . Для загрузки демонстрационного каталога в пустую базу:

```powershell
.\.venv\Scripts\python.exe manage.py loaddata fixtures/goods/categories.json fixtures/goods/products.json
```

Файл `.env`, виртуальное окружение, кэш, резервные копии и фотографии пользователей исключены из Git. Каталог и изображения товаров включены. Настройка `DJANGO_DEBUG=True` предназначена для локальной разработки; публикация кода на GitHub сама по себе не запускает сайт в интернете.
