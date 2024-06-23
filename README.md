## Как запустить проект:
### Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/Mikhail0-O/api_final_yatube.git

cd kittygram
```
### Cоздать и активировать виртуальное окружение:
```
python -m venv venv

source venv/Scripts/activate
```
### Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip

pip install -r requirements.txt
```
### Выполнить миграции:
```
python3 manage.py migrate
```
### Запустить проект:
```
python3 manage.py runserver
```