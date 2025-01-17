# Данный проект позволяет собирать информацию о мероприятиях.

## Источник данных: 
- https://conferencemonkey.org/

## Общая архитектура
- [api_service](api_service) - сервис для взаимодействия с собранными данными
- [database](database) - persistent хранилище для базы данных (был выбран postgres, так как классика)
- [events_scrapper](events_scrapper) - используется для сбора информации о новых ивентах
  - [models](events_scrapper%2Fscrapper%2Fmodels) - используемые модели
  - [engines](events_scrapper%2Fscrapper%2Fengines) - доступные движки сбора (реализован 1)
  - [utils](events_scrapper%2Futils) - полу-пустой модуль, содержащий полезные инструменты

## Основная логика работы
### Запуск скрипта
Необходимо выполнить docker compose build & up

После необходимо вручную применить миграции из директории events_scrapper/ddl/. Автоматические миграции не сделаны, так как обычно это делается через CI/CD через модуль yoyo

Все остальные сервисы поднимутся сами по себе.

При желании можно менять исходный код с помощью IDE и перезапускать сервис (например через Docker Desktop). (подтянуты volumes)

Потенциально возможны проблемы с установленными зависимостями, поэтому рекомендуется сначала проверить локально. (Шанс мал, но есть)

### DDL
Можно посмотреть самостоятельно после поднятого докера и примененных миграций

### Архитектура API
Я захотел вспомнить не Object подход (обычно использую LiteStar), поэтому выбрал FastApi. Все сделано по классике, swagger доступен по адресу localhost:9000/docs.

CLI интерфейс не реализован, так как по моему опыту это очень устаревший подход.

### Архитектура скраппера
Имеется ABC Engine, от которого наследуются все возможные скрапперы. В данном скрипте реализован сборщик для сайта указанного выше. Абстрактные методы можно посмотреть по коду

Имеется класс Scheduler который запускает бесконечный цикл на поиск и процесс новых событий.

Бекап системы сделан через дополнительную табличку. При запуске Scheduler забирает последний url вытащенный machine_id. Данный url является критерием остановки. Важно отметить что система не предусматривает ситуацию при которой ранее существующее событие было удалено. Это достаточно легко реализовать (бегать по всем страницам до конца), но для этого необходимо написать дополнительную логику

### Общие слова
По коду расставлено некоторое количество TODO/FIXME (не полное количество наблюдений). Все эти места легко дорабатываются при условии наличия времени.

Код не соответствует DRY, так как в целях экономии времени разворачивается в контексте одного docker compose. Правильным решением было бы разнесение модулей в отдельные сервисы. Самое банальное, весь инструментарий должен быть снесен с отдельный пакет устанавливающийся через pip install

Так же не было нормального ведения git журнала (по стандарту conventional commits). Думаю не стоит объяснять что при разработке одним человеком от таких стандартов можно спокойно отходить.

Еще следует отметить отсутствие линтера, в силу ограниченного времени.
## Главные предположения
- Если добавляется новое событие - оно добавляется в начало страницы
- События имеют постоянную структуру detailed page
- Нельзя упереться в ограничение по запросам
- Сайт статичен
- В базе содержится URL записи до которой можно дойти переходя по страницам вида: https://conferencemonkey.org/top/conferences?page=1. Данная запись является критерием останова

Касательно последнего пункта - это означает что следует положить в таблицу следующую запись (последняя доступная запись)
- machine_id: 1
- last_saved_url: https://conferencemonkey.org/conference/federal-reserve-bank-of-cleveland-undergraduate-research-conference-1532398,
- last_saved_time: 2024-04-16 00:51:35.454069 (можно выбрать самостоятельно. Главное чтобы значение было валидно, а именно меньше чем сейчас. Важно что используется формат UTC)
