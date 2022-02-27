# Notes

----

Web application for notes.

----
Requirements:
- Python: version 3.10.2
- Libraries: requirements.txt

----

Запуск локальной версии проекта:
- Склонировать проект ( git clone ...)
- В директории проекта собрать docker - образ ( docker-compose build )
- Запустить docker образ ( docker-compose up )
- Применить миграции ( docker-compose run app python manage.py migrate )
