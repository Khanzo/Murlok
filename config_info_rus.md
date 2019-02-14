# Murlok Configuration info RUS
Описание файла конфигурации паука.<br>
Секции файла, на примере habr.xml.<br>

Наименование паука: <name>habrSpider</name><br>
Стартовый url-адрес: <start_url>https://habr.com/ru/all/</start_url><br>
Выходной формат: <format>mysql</format><br>
Возможные форматы:<br>
* в файл - json, xml, jsonlines, csv, pickle, marshal<br>
* в базу данных - mysql, postg, sqlite<br>

Дальше идет секция описания подключения к базе данных, если в качестве выходного формата используется база данных,<br>
база и таблица должна быть создана заранее<br>
<peewee параметры>поля таблицы</peewee><br>

Параметры:<br>
- host - адрес подключения к базе данных<br>
- user - пользователь базы данных<br>
- pass - пароль пользователя базы данных<br>
- port - порт подключения к базе данных, если не указан, то по умолчанию mysql - 3316, postg - 5432<br>
- charset - кодировка базы данных / пока не используется и можно не указывать<br>
- db - наименование базы данных, для Sqlite наименование файла базы данных<br>
- table - таблица<br>

Пример подключения к MySQL базе vkit, таблица habr:<br>
<peewee host="127.0.0.1" user="root" pass="" port="3306" charset="utf8mb4" db="vkit" table="habr"><br>
Пример подключения к Sqlite базе vkit, таблица habr:<br>
<peewee db="vkit.db" table="habr"><br>

Поля таблицы:<br>
в секции - <tablefields></tablefields> - описывают соотношение полей свойств <properties> и таблицы базы данных<br>
<field name="имя в таблице" property_name="имя свойства" default="по умолчанию" type="тип"></field><br>
если property_name не указано, то оно равно name<br>
type - типы данных: str, int (строка и число)<br>
default - можно указать значение по умолчанию<br>
Поле создания кэша, для создания уникального поля - name="cashe" - создает строку-кэш по значению поля cashe_field<br>

Пример:<br>
<tablefields><br>
<field name="title" property_name="title"></field><br>
<field name="url_post" property_name="url_post"></field><br>
<field name="date" property_name="date"></field><br>
<field name="avtor" property_name="avtor"></field><br>
<field name="published" property_name="" default="0" type="int"></field><br>
<field name="cashe" property_name="" cashe_field="title"></field><br>
</tablefields><br>

Затем идут поля настроек паука:<br>
- <encoding></encoding> - можно указать кодировку, по умолчанию utf-8<br>
- <agent></agent> - описание свойств агента-паука, по умолчанию: Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0<br>

Далее идут поля настроек обхода пауком страниц:
- <selector>article.post_preview</selector> - селектор выбора информационных блоков, откуда будут извлекаться данные<br>
- <nextselector></nextselector> - селектор поиска следующей страницы<br>
- <maxpage>2</maxpage> - максимальное кол-во страниц, которое будет пройдено, по умолчанию 1, если указан 0, то будет пытаться обойти все<br>
- <nextpage>https://habr.com/ru/all/page</nextpage> - основа для генерации адреса следующей страницы с использованием счетчика:<br>
next_page = nextpage + str(counter) - https://habr.com/ru/all/page1, https://habr.com/ru/all/page2 и тд.<br>
- <endselector></endselector> - селектор остановки, если он будет найдет на странице, то паук остановится

Пример из glamour.xml:<br>
<selector>ul.c-card-section__card-list li</selector><br>
<maxpage>0</maxpage><br>
<nextpage></nextpage><br>
<nextselector></nextselector><br>
<endselector></endselector><br>
Так как не указано, как перейти дальше, то паук отпарсит только стартовый адрес.<br>

Затем начинается секция <properties></properties> - описание свойств данных и как их получить из селектора выбора информационных блоков.<br>
Поле данных описывается в секции <property></property> следующим образом, на примере habr.xml:<br>
<property><br>
<name>title</name> - наименование свойства<br>
<before></before> - можно вставить текст, который будет перед значением данных<br>
<selector>h2.post__title a::text</selector> - селектор отбора данных - он может и отсуствовать. Если он равен Now, - то значение станет равно текущей дате в формате %d-%m-%Y<br>
<after></after> - можно вставить текст, который будет после значения данных<br>
<replace_filters></replace_filters> - секция фильтров, может быть пуста<br>
</property><br>

Секция фильтров <replace_filters></replace_filters>, состоит из секций:<br>
<filter><old>старое значение</old><new>новое значение</new></filter> - где указано, какие данные в значении будут заменены и на что<br>

Пример из glamour.xml:<br>
<property><br>
<name>url_img</name><br>
<before></before><br>
<selector>div.c-card__image noscript</selector><br>
<after></after><br>
<replace_filters><br>
<filter><old>noscript</old><new></new></filter> - удалит noscript(значение <old>noscript</old>) из текста значения данных<br>
<filter><old>&gt;</old><new></new></filter> - удалит &gt;(значение <old>&gt;</old>) из текста значения данных<br>
<filter><old>&quot;</old><new>"</new></filter> - заменит &quot;(значение <old>&quot;</old>) на " (значение <new>"</new>) в тексте значения данных<br>
</replace_filters><br>
</property><br>

Пример из glamour.xml:<br>
<property><br>
<name>site</name><br>
<before>www.glamourmagazine.co.uk</before><br>
<selector></selector><br>
<after></after><br>
<replace_filters></replace_filters><br>
</property><br>
Значение поля site будет равно www.glamourmagazine.co.uk<br>

<property><br>
<name>date</name><br>
<before></before><br>
<selector>Now</selector><br>
<after></after><br>
<replace_filters></replace_filters><br>
</property><br>
Значение поля date будет равно текущей дате в формате %d-%m-%Y

