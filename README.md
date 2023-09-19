# Tracking the dynamics of currencies.
Описание проекта ниже в пункте "ТЗ".

Запуск:
- Клонировать репозиторий.
- В sibdev_project/.env изменить данные для postgres, rabbitmq, email.
- Запустить команду "docker-compose up --build" из корня проекта. Сервис будет доступен по адресу "http://0.0.0.0:8000/api/v1"
- Пункт №6 из ТЗ ниже. Для загрузки архива данных использовать команды "docker ps -a", скопировать <container_id> контейнера "sibdev_drf", ввести команду "docker exec -it <conteiner_id> python django_app.py download_archive". После этого загрузятся все доступные данные за последние 30 дней.
- Используется Bearer Authentication.

Эндпоинты:
- http://0.0.0.0:8000/api/v1/user/register/ - Регистрация пользователя по почте и паролю. Ожидает JSON в формате {"email": "email@email.com", "password": 1234/"1234qwer"}.
- http://0.0.0.0:8000/api/v1/user/login/ - Получение JWT токена по почте и паролю указанных при регистрации.
- http://0.0.0.0:8000/api/v1/rates/ | http://0.0.0.0:8000/api/v1/rates/?value=value or -value - Получение всех последних загруженных котировок для анонимных пользователей. Для авторизованнх пользователей возвращает список отслеживаемых валют. При указании значения "value" вовращается отсортированный список по возрастанию или убыванию.
- http://0.0.0.0:8000/api/v1/currency/user_currency/ - POST запрос на добавление отслеживаемых валют. Только для авторизованных пользователей. Ожидает JSON в формате {"currency": 1(id валюты), "threshold": 100/100.0 (ПЗ)}.
- http://0.0.0.0:8000/api/v1/currency/<int:id>/analytic?date_from=year-month-day&date_to=year-month-day&threshold=int or float - Возвращает список с расширенными полями для аналитики. id = id валюты, date_from = дата начала диапазона для выгрузки, date_to = дата окончания диапазона для выгрузки, threshold = ожидаемая цена валюты.


ТЗ:

![ALT TEXT](https://github.com/mrPechen/test_task_sibdev/blob/main/tz.png)
