### Описание
API для блога. Можно писать свои посты. Комментровать посты.
Подписываться на авторов постов. 
Также предусмотрена регистрация пользователей (JWT+djoser)

### Аутентификация
Для доступа ко многим эндпоинтам требуется аутентификация. Вам необходимо включить API ключ в заголовки ваших запросов:
```
Authorization: Bearer ВАШ_API_КЛЮЧ
```

### Эндпоинты
Получение всех постов:
URL: http://127.0.0.1:8000/api/v1/posts/
Метод: GET
Параметры:
limit (необязательный): Количество элементов на странице.
offset (необязательный): Элементы начиная с offset + 1
Пример:
```
GET /widgets?page=1&limit=10
```
Ответ:
```
{
    "count": 0,
    "next": null,
    "previous": null,
    "results": []
}
```

### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/Mikhail0-O/api_final_yatube.git

cd kittygram
```
Cоздать и активировать виртуальное окружение:
```
python -m venv venv

source venv/Scripts/activate
```
Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip

pip install -r requirements.txt
```
Выполнить миграции:
```
python manage.py migrate
```
Запустить проект:
```
python manage.py runserver
```