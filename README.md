# test_shop

## Api для оформления заказа в интернет магазине

Проект разбит на 3 сервиса, сервис аутентификации, сервис заказов и каталог товаров.
Основной сервис заказов реализован на Django, другие 2 на Fastapi.

Делал масксимально просто, опущена регистрация пользователей, предполагается, что они у нас уже имеются.
Визуального интерфейса нет, все операции производятся путем запросов.

Запуск приложения стандартный:<br/>
docker-compose -f docker-compose.dev.yml build - собираем<br/>
docker-compose -f docker-compose.dev.yml up -d - запускаем

Так как пользователи уже есть в базе, производим логин одного из них.
Пользователи-пароли находятся в users.txt

Авторизуемся на сервере запросом вида:<br/>
***curl -X POST "http://0.0.0.0:80/auth/token" -H "accept: application/json" -H "Content-Type: application/x-www-form-urlencoded" -d "username=username&password=pass"***

В ответ придет временный токен, с помощью которого можно взаимодействовать с апи.

Получить список продутов:<br/>
***curl -H "Accept: application/json" http://0.0.0.0:80/catalog/all***

После можно отправить запрос вида:<br/>
***curl --dump-header - -H "Content-Type: application/json" -H "Authorization: Bearer TOKEN" -X POST --data '{"products": [{"id": ID, "count": COUNT}, {"id": ID, "count": COUNT}]}' http://0.0.0.0:80/api/order/***

Тем самым мы создаем заказ, последующие запросы его редактируют

Просмотр заказа:
***curl -H "Accept: application/json" -H "Authorization: Bearer TOKEN" http://0.0.0.0:80/api/order/***


Просмотр информации о пользователе:
***curl -X GET "http://0.0.0.0:80/auth/user/ID" -H "accept: application/json"***


