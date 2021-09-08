# IQTEK
На любом python фреймворке (FastAPI, Flask и т.д.) или без реализуйте REST API сервис, реализующий операции над сущностью User с полями - id, ФИО.

Сервис предполагает:


создание User, 


изменение User, 


получение по id,


удаление User.


Технические требования:

Необходимы несколько реализаций репозитория - в памяти и БД (mysql, postgress или иные). Реализация репозитория выбирается при инициализации приложения из конфиг файла, с указанием типа репозитория и его настройками (доступы).


Использование ООП

Особое внимание стоит обратить на следующие моменты:

Код должен быть написан понятно и аккуратно, с соблюдением табуляции и прочих элементов написания, без лишних элементов и функций, не имеющих отношения к функционалу тестового задания, снабжен понятными комментариями.

Читабельность и наличие элементарной архитектуры.
Чистота и оформление кода — не менее важный фактор. Код должен быть написан в едином стиле (желательно в рекомендуемом для конкретного языка). Также к чистоте относятся отсутствие копипаста и дублирования логики.

Тестовое задание должно быть представлено в следующем виде:

Ссылка на публичный репозиторий GitHub с исходным кодом.

Отправку результата оформить как pull request для пользователя iqtek

**Требования приложения**
mysql 8.0.26

*библиотеки*
flask==2.0.1
Werkzeug~=2.0.1

## REST API запросы

**Создание пользователя**
