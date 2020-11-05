# currency-app
Minimal currency app for test task

## Описание
Во время разработки было создано два api метода:

    /showcurrency

Выводит словарь со всеми доступными валютами, где ключ - символьный код валюты, а значение - название валюты.

    /diff
 с параметрами:
 
* char_code - символьный код валюты
* date_first - дата в формате YYYY-MM-DD
* date_second - дата в формате YYYY-MM-DD

Выводит словарь с датами и разницей курса валюты к рублю

Оба метода используют GET запросы на сайт центробанка

## Ресурсы
Были использованы библиотеки:

* requests - для запросов
* xml - для парсинга и обработки данных с сайта центробанка
* flask  - для создания веб приложения
* flask_restful для создания api

## Пример использования приложения
    /showcurrency
![cur list](https://user-images.githubusercontent.com/47665637/98214812-05cf8000-1f58-11eb-936c-0a219097bd28.PNG)

    /diff?char_code=GBP&date_first=2002-03-02&date_second=2003-03-01
    
![diff list](https://user-images.githubusercontent.com/47665637/98214861-17188c80-1f58-11eb-815a-65ab8c61f833.PNG)
