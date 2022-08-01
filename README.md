## как запустить скрипт
1. скачиваем Chromedriver по [ссылке](https://chromedriver.storage.googleapis.com/index.html). 

*важно, чтобы первые числа версий драйвера и браузера на вашем компьютере совпадали*

>### как проверить версию браузера
> 
> открываем браузер > настройки > о браузере

2. создаём проект
> pycharm > file > new project > create
3. создаём директорию под драйвер
> pycharm > правой кнопкой мыши по названию проекта в меню слева > new > directory > 
> вводим название > [распаковываем драйвер](https://selenium-python.com/install-chromedriver-chrome#:~:text=%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%20ChromeDriver%20%D0%BF%D0%BE%D0%B4%20Linux%2C%20Windows%20%D0%B8%20Mac)
4. устанавливаем selenium, прописывая `pip install selenium` в терминал пайчарма
5. устанавливаем pandas, прописывая `pip install pandas` туда же
6. в переменную `s` вставляем ваш путь до драйвера
> в pycharm в меню слева находим файл драйвера > нажимаем правой кнопкой мыши > copy path > absolute path
7. запускаем код
8. результат можно посмотреть в создавшемся файле NFT.csv *(у вас он будет отличаться от моего)*
