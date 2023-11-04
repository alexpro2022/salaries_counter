# salaries_counter

[Тестовое задание](https://docs.google.com/document/d/1XRR5m0PMocZf-AwM1BFNYUJ2OdBEkm9YYH8uQjYlvQc/edit)

<br>

## Оглавление:
- [Технологии](#технологии)
- [Описание работы](#описание-работы)
- [Установка и запуск](#установка-и-запуск)
- [Удаление](#удаление)
- [Автор](#автор)

<br>

## Технологии:

[![Python](https://img.shields.io/badge/Python-v3.11-blue?logo=python)](https://www.python.org/)
[![asyncio](https://img.shields.io/badge/-asyncio-464646?logo=python)](https://docs.python.org/3/library/asyncio.html)
[![aiogram](https://img.shields.io/badge/aiogram-v3.1-blue?logo=aiogram)](https://aiogram.dev/)
[![aiohttp](https://img.shields.io/badge/-aiohttp-464646?logo=aiohttp)](https://docs.aiohttp.org/en/stable/index.html)
[![Pydantic](https://img.shields.io/badge/-Pydantic-464646?logo=Pydantic)](https://docs.pydantic.dev/)
[![MongoDB](https://img.shields.io/badge/-MongoDB-464646?logo=MongoDB)](https://www.mongodb.com/)
[![Motor](https://img.shields.io/badge/-Motor-464646?logo=Python)](https://motor.readthedocs.io/en/3.3.1/)
[![docker_compose](https://img.shields.io/badge/-Docker%20Compose-464646?logo=docker)](https://docs.docker.com/compose/)
[![Telegram](https://img.shields.io/badge/-Telegram-464646?logo=Telegram)](https://core.telegram.org/api)

[⬆️Оглавление](#оглавление)

<br>

## Описание работы:
В данной работе реализован телеграм-бот, который принимает от пользователей текстовые сообщения содержащие JSON с входными данными и отдает агрегированные данные в ответ. Вычисления производятся с помощью алгоритма агрегации статистических данных о зарплатах сотрудников компании по временным промежуткам (реализован на основе  запросов к БД MongoDB). 
Телеграм-бот принимает и передает на вход алгоритма следующие данные:
  - дату и время старта агрегации в ISO формате
  - дату и время окончания агрегации в ISO формате
  - тип агрегации (могут быть следующие типы: hour, day, month)

Алгоритм формирует и передает боту ответ, содержащий:
  - агрегированный массив данных
  - подписи к значениям агрегированного массива данных в ISO формате. 
Вычисления производятся на основе статистических данных из [коллекции](https://drive.google.com/file/d/1pcNm2TAtXHO4JIad9dkzpbNc4q7NoYkx/view?usp=sharing):

[⬆️Оглавление](#оглавление)

<br>

## Установка и запуск: 
#### Docker Compose
<details><summary>Предварительные условия:</summary>

Предполагается, что пользователь:
 - создал [бота](https://github.com/alexpro2022/instructions-t-bot/blob/main/README.md#%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5-%D0%B8-%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0-%D0%B0%D0%BA%D0%BA%D0%B0%D1%83%D0%BD%D1%82%D0%B0-%D0%B1%D0%BE%D1%82%D0%B0)

 - установил [Docker](https://docs.docker.com/engine/install/) и [Docker Compose](https://docs.docker.com/compose/install/) на локальной машине или на удаленном сервере, где проект будет запускаться в контейнерах. Проверить наличие можно выполнив команды:
 
    ```bash
    docker --version && docker-compose --version
    ```
<h1></h1>
</details>
<br>

1. Клонируйте репозиторий с GitHub и введите данные для переменных окружения (обязательное значение - `BOT_TOKEN`):

```bash
git clone https://github.com/alexpro2022/salaries_counter.git
cd salaries_counter
cp env_example .env
nano .env
```

2. После клонирования репозитория необходимо загрузить [bson-файл](https://drive.google.com/file/d/1pcNm2TAtXHO4JIad9dkzpbNc4q7NoYkx/view?usp=sharing) и поместить его в папку `data` под именем `sample-collection.bson` в корне проекта (`data/sample-collection.bson`).

3. Из корневой директории проекта выполните команду:
```bash
docker compose up -d --build
```
Проект будет развернут в docker-контейнерах, (контейнеры бота и доступа к БД будут ожидать завершения загрузки статистических данных из коллекции). Далее:
  - Доступ к БД осуществляется по адресу: http://localhost:8081/
  - Запустите своего телеграм-бота командой `/start`

4. Остановить docker и удалить контейнеры можно командой из корневой директории проекта:
```bash
docker compose down
```
Если также необходимо удалить тома базы данных, статики и медиа:
```bash
docker compose down -v
```

[⬆️Оглавление](#оглавление)

<br>

## Удаление:
Из корневой директории проекта выполните команду:
```bash
cd .. && rm -fr salaries_counter
```
  
[⬆️Оглавление](#оглавление)

<br>

## Автор:
[Aleksei Proskuriakov](https://github.com/alexpro2022)

[⬆️В начало](#salaries_counter)