# Проект “Обмен валют”

REST API для описания валют и обменных курсов. Позволяет просматривать и редактировать списки валют и обменных курсов, и совершать расчёт конвертации произвольных сумм из одной валюты в другую.

[Веб-интерфейс](https://github.com/zhukovsd/currency-exchange-frontend) взят из технического задания.

[Техническое задание проекта](https://zhukovsd.github.io/python-backend-learning-course/projects/currency-exchange/)

## Варианты запуска приложения:

#### 1. Через Docker

(Предполагается что Docker desctop установлен и запущен)

Измените настройки frontend, файл app.js в папке frontend/js
```
const host = "http://ваш_ip/api"
```
Измените настройки nginx, файл nginx.conf в главной папке
```
server_name  ваш_ip;
```
Запустите докер с помощью консоли:
```
docker-compose up --build
```
Теперь сайт будет доступен по адресу http://ваш_ip/

#### 2. Через терминал

Измените .env файл в папке backend:
```
SERVER_HOST='127.0.0.1'
```
Измените настройки frontend, файл app.js в папке frontend/js
```
const host = "http://127.0.0.1:8888/"
```
Установите необходимые библиотеки и запустите виртуальное окружение
```
python3 -m pip install --upgrade pip && pip install uv
uv venv /app/.venv
uv sync
```
Активируйте venv
```
.\.venv\scripts\activate
```
Запустите backend:
```
python backend/main.py
```
Теперь вы можете:
    Взаимодействовать с API напрямую через запросы по адресу http://127.0.0.1:8888/.
    Использовать сайт, который находится по адресу frontend/index.html.


#### 3. Запуск тестов

Измените настройки frontend, файл app.js в папке frontend/js
```
const host = "http://127.0.0.1:8888/"
```
Установите необходимые библиотеки и запустите виртуальное окружение
```
python3 -m pip install --upgrade pip 
pip install uv
uv venv /app/.venv
uv sync
```
Активируйте venv
```
.\.venv\scripts\activate
```
Запустите тестовый backend:
```
python backend/src/tests/main.py
```
Теперь можно запустить тесты:
```
pytest backend/src/tests/test_api.py
```


Также доступен сайт, на котором уже запущено приложение: http://185.21.156.184:8888/

## REST API

#### GET `/currencies`

Получение списка валют. Пример ответа:
```
[
    {
        "id": 0,
        "name": "United States dollar",
        "code": "USD",
        "sign": "$"
    },   
    {
        "id": 0,
        "name": "Euro",
        "code": "EUR",
        "sign": "€"
    }
]
```

HTTP коды ответов:
- Успех - 200
- Ошибка (например, база данных недоступна) - 500

#### GET `/currency/EUR`

Получение конкретной валюты. Пример ответа:
```
{
    "id": 0,
    "name": "Euro",
    "code": "EUR",
    "sign": "€"
}
```

HTTP коды ответов:
- Успех - 200
- Код валюты отсутствует в адресе - 400
- Валюта не найдена - 404
- Ошибка (например, база данных недоступна) - 500

#### POST `/currencies`

Добавление новой валюты в базу. Данные передаются в теле запроса в виде полей формы (`x-www-form-urlencoded`). Поля формы - `name`, `code`, `sign`. Пример ответа - JSON представление вставленной в базу записи, включая её ID:
```
{
    "id": 0,
    "name": "Euro",
    "code": "EUR",
    "sign": "€"
}
```

HTTP коды ответов:
- Успех - 200
- Отсутствует нужное поле формы/ неправильный формат ввода - 400
- Валюта с таким кодом уже существует - 409
- Ошибка (например, база данных недоступна) - 500

### Обменные курсы

#### GET `/exchangeRates`

Получение списка всех обменных курсов. Пример ответа:
```
[
    {
        "id": 0,
        "baseCurrency": {
            "id": 0,
            "name": "United States dollar",
            "code": "USD",
            "sign": "$"
        },
        "targetCurrency": {
            "id": 1,
            "name": "Euro",
            "code": "EUR",
            "sign": "€"
        },
        "rate": 0.99
    }
]
```

HTTP коды ответов:
- Успех - 200
- Ошибка (например, база данных недоступна) - 500

#### GET `/exchangeRate/USDRUB`

Получение конкретного обменного курса. Валютная пара задаётся идущими подряд кодами валют в адресе запроса. Пример ответа:
```
{
    "id": 0,
    "baseCurrency": {
        "id": 0,
        "name": "United States dollar",
        "code": "USD",
        "sign": "$"
    },
    "targetCurrency": {
        "id": 1,
        "name": "Euro",
        "code": "EUR",
        "sign": "€"
    },
    "rate": 0.99
}

```

HTTP коды ответов:
- Успех - 200
- Коды валют пары отсутствуют в адресе - 400
- Обменный курс для пары не найден - 404
- Ошибка (например, база данных недоступна) - 500

#### POST `/exchangeRates`

Добавление нового обменного курса в базу. Данные передаются в теле запроса в виде полей формы (`x-www-form-urlencoded`). Поля формы - `baseCurrencyCode`, `targetCurrencyCode`, `rate`. Пример полей формы:
- `baseCurrencyCode` - USD
- `targetCurrencyCode` - EUR
- `rate` - 0.99

Пример ответа - JSON представление вставленной в базу записи, включая её ID:
```
{
    "id": 0,
    "baseCurrency": {
        "id": 0,
        "name": "United States dollar",
        "code": "USD",
        "sign": "$"
    },
    "targetCurrency": {
        "id": 1,
        "name": "Euro",
        "code": "EUR",
        "sign": "€"
    },
    "rate": 0.99
}
```

HTTP коды ответов:
- Успех - 200
- Отсутствует нужное поле формы/ неправильный формат ввода - 400
- Валютная пара с таким кодом уже существует - 409
- Одна (или обе) валюта из валютной пары не существует в БД - 404
- Ошибка (например, база данных недоступна) - 500

#### PATCH `/exchangeRate/USDRUB`

Обновление существующего в базе обменного курса. Валютная пара задаётся идущими подряд кодами валют в адресе запроса. Данные передаются в теле запроса в виде полей формы (`x-www-form-urlencoded`). Единственное поле формы - `rate`.

Пример ответа - JSON представление обновлённой записи в базе данных, включая её ID:
```
{
    "id": 0,
    "baseCurrency": {
        "id": 0,
        "name": "United States dollar",
        "code": "USD",
        "sign": "$"
    },
    "targetCurrency": {
        "id": 1,
        "name": "Euro",
        "code": "EUR",
        "sign": "€"
    },
    "rate": 0.99
}

```

HTTP коды ответов:
- Успех - 200
- Отсутствует нужное поле формы/ неправильный формат ввода - 400
- Валютная пара отсутствует в базе данных - 404
- Ошибка (например, база данных недоступна) - 500

### Обмен валюты

#### GET `/exchange?from=BASE_CURRENCY_CODE&to=TARGET_CURRENCY_CODE&amount=$AMOUNT`

Расчёт перевода определённого количества средств из одной валюты в другую. Пример запроса - GET `/exchange?from=USD&to=AUD&amount=10`.

Пример ответа:
```
{
    "baseCurrency": {
        "id": 0,
        "name": "United States dollar",
        "code": "USD",
        "sign": "$"
    },
    "targetCurrency": {
        "id": 1,
        "name": "Australian dollar",
        "code": "AUD",
        "sign": "A€"
    },
    "rate": 1.45,
    "amount": 10.00
    "convertedAmount": 14.50
}
```
---

Для всех запросов, в случае ошибки, ответ:
```
{
    "code": (код ошибки), 
    "status": "Ошибка", 
    "message": (Информация обо ошибке)
}
```
