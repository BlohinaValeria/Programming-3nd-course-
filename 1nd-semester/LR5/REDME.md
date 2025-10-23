# Лабораторная работа 5. RPC. gRPC. Protobuf

На основе продемонстрированного примера и мини-проекта с реализацией двух сервисов (рекомендация книг), реализуйте приложение, аналогичное приложение из задания 4, с использованием gRPC, protobuf.  Предоставьте ссылку на репозиторий GitHub со всеми необходимыми компонентами для развертывания. При возможности, разверните словарь на публичном сервере в вебе. 
В репозитории отразите отчет с помощью файла с разметкой Markdown, где демонстрировался бы процесс развертывания и работы сервиса.
Формулировка задания
Создать полный глоссарий употребляемых терминов по какой-то области (допустим, Python) и спроектировать доступ к нему в виде  Web API в докер-контейнере по образцу brendanburns/dictionary-server (или в иной форме отчуждения/контейнеризации, допускающей быстрое развёртывание на произвольной платформе). 

## Структура проекта
![перейти](https://github.com/BlohinaValeria/Programming-3nd-course-/blob/main/1nd-semester/LR5/структура%20.png)

## Комментарии к решению 
:small_red_triangle_down: разделение клиентской и серверной части 
:small_red_triangle_down: подгрузка зависимостей в обеих частях
:small_red_triangle_down: собран общий Dockerfile

## Proto
![перейти](https://github.com/BlohinaValeria/Programming-3nd-course-/blob/main/1nd-semester/LR5/proto%201.png)

## Запуск контейнера
![перейти](https://github.com/BlohinaValeria/Programming-3nd-course-/blob/main/1nd-semester/LR5/запуск%20сервера.png)

## Итог развертывания
![перейти](https://github.com/BlohinaValeria/Programming-3nd-course-/blob/main/1nd-semester/LR5/итог.png)
## Комментарии к решению 
:small_red_triangle_down: добавлен index.html с удобным интерфейсом для просмотра терминов 
