# Сервис записи пациентов в клинике

На машине (подразумевается linux) для запуска должен быть установлен Docker и Git

## Запуск

Забрать проект с GitHub 
```bash
git clone https://github.com/fakeface2117/clinics_project.git
```
Если гита нет, то установить его
```bash
sudo apt update
sudo apt install git -y
```
Перейти в директорию с проектом
```bash
cd  clinics_project
```
Сделать билд образа приложения
```bash
docker compose build
```
Создать файл конфигурации `.env` из примера `.env.example`
```bash
cat .env.example >> .env
```
Запуск приложения и Postgres через compose (либо в режиме демона с флагом -`d`)
```bash
docker compose up
```
- Должны появиться логи запущенного приложения и БД
- После успешного запуска нужно в браузере перейти в Swagger по адресу `http://your_host:8000/appointments/openapi` для просмотра документации и вызова API-endpoints. Здесь `your_host` это `ip-адрес` машины, откуда запускалось приложение
- В документации можно перейти в Админ-панель

Остановить приложение `ctrl+c` или выполнить команду `docker compose stop`

## Дополнительный материал по заданию

[Док-артефакты](doc_artefacts%2FREADME.md)

[Telegram-бот (концепция)](telegram_bot%2FREADME.md)
