# Message bot

Simple telegram and vk callback api message bot.

### Предварительные требования
- Сервер Ubuntu 16.04 LTS
- Домен второго уровня привязанный к серверу (Указаны A-записи, указывающие на IP-адрес сервера для @.<домен.ru> и *.<домен.ru>
- Создана и настроена группа вк
- Создан и настроен бот в Telegram

### Настройка директорий и пользователя
Создать директорию пользователя
```sh
$ sudo mkdir /var/www
$ sudo mkdir /var/www/django
```

Создать пользователя
```sh
$ sudo useradd -d /var/www/django django
$ sudo passwd django
```

Добавить пользователя в sudoers
```sh
$ sudo nano /etc/sudoers
```

В конец файла добавить
```sh
django  ALL=(ALL) ALL
```

Поменять владельца папки пользователя
```sh
$ sudo chown django:django /var/www/django
```

Поменять текущего пользователя
```sh
$ su django
```

Создать директории
```sh
$ mkdir /var/www/django/project
$ mkdir /var/www/django/tmp
$ mkdir /var/www/django/logs
$ mkdir /var/www/django/data
```

Создать директории
```sh
$ mkdir /var/www/django/project
$ mkdir /var/www/django/tmp
$ mkdir /var/www/django/logs
$ mkdir /var/www/django/data
```

### Установка Nginx и настройка SSL-соединения
Удалить apache2
```sh
$ sudo apt-get remove apache2
```

Установить nginx
```sh
$ sudo add-apt-repository ppa:nginx/development
$ sudo apt-get update
$ sudo apt-get install nginx -y
```

Установить certbot ([Инструкция](https://certbot.eff.org/#ubuntuxenial-nginx))
```sh
$ sudo apt-get install software-properties-common
$ sudo add-apt-repository ppa:certbot/certbot
$ sudo apt-get update
$ sudo apt-get install certbot 
```

Открыть файл
```sh
$ sudo nano /etc/nginx/sites-available/default
```
Добавить строчку в блоке server
```sh
location ~ /.well-known {
    allow all;
}
```

Протестируйте конфигурационный файл Nginx на корректность
```sh
$ sudo nginx -t
```

Должны вернуться следующие значения
```sh
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

Перезапустите Nginx
```sh
$ sudo service nginx reload
```

Перезапустите Nginx
```sh
$ sudo service nginx reload
```

Сделать SSL сертификат
```sh
$ sudo certonly -a webroot --webroot-path=/var/www/html -d домен.ru -d www.домен.ru
```

Генерация параметров Диффи-Хеллмана
```sh
$ sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
```

Заменить /etc/nginx/nginx.conf  из configuration/nginx.conf и  /etc/nginx/site-enabled/default из configuration/vhost_ssl.conf
Поправить домены в default

Перезапустить nginx
```sh
$ sudo service nginx reload
```

Добавить автообновление сертификата каждые 30 дней, открыть крон
```sh
$ crontab -e
```

Добавить строчки в конец файла
```sh
30 5 * * 1 sudo letsencrypt renew
35 5 * * 1 sudo service nginx reload
```
