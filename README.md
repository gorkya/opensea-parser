## как запустить скрипт
1. скачиваем Chromedriver по [ссылке](https://chromedriver.storage.googleapis.com/index.html). 

*важно, чтобы первые числа версий драйвера и браузера на вашем компьютере совпадали*

>### как проверить версию браузера
> 
> открываем браузер > настройки > о браузере

2. создаём директорию под драйвер
>pycharm > правой кнопкой мыши по названию проекта в меню слева > new > directory > 
> вводим название > [распаковываем драйвер](https://selenium-python.com/install-chromedriver-chrome#:~:text=%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%20ChromeDriver%20%D0%BF%D0%BE%D0%B4%20Linux%2C%20Windows%20%D0%B8%20Mac)
3. устанавливаем selenium, прописывая `pip install selenium` в терминал пайчарма
4. устанавливаем pandas, прописывая `pip install pandas` туда же
5. в переменную `s` вставляем ваш путь до драйвера
6. запускаем код
