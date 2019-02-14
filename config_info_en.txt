# Murlok Configuration info EN (Yandex Translate)
Описание файла конфигурации паука.<br>
Sections of the file, for example habr.xml.<br>

The name of the spider: <name>habrSpider</name><br>
Starting url-address: <start_url>https://habr.com/ru/all/</start_url><br>
Output format: <format>mysql</format><br>
Possible format:<br>
* into a file - json, xml, jsonlines, csv, pickle, marshal<br>
* into the database - mysql, postg, sqlite<br>

Next is the database connection description section, if you use the database as the output format,<br>
the base and table must be created in advance<br>
<peewee parameters>table field</peewee><br>

Parameters:<br>
- host - address of the database connection<br>
- user - database user<br>
- pass - password of the database user<br>
- port - database connection port, if not specified, default mysql-3316, postg-5432<br>
- charset-database encoding / not yet used and can be omitted<br>
- db - database name, for Sqlite database file name<br>
- table - table<br>

Example of connection to MySQL database vkit, table habr:<br>
<peewee host="127.0.0.1" user="root" pass="" port="3306" charset="utf8mb4" db="vkit" table="habr"><br>
Example of connection to Sqlite database vkit, habr table:<br>
<peewee db="vkit.db" table="habr"><br>

Table fields:<br>
<table fields></table fields> - the section describes the relationship between the property fields <properties> and the database table<br>
<field name= "table name" property_name= "property name" default= "default" type= "type" ></field><br>
if property_name is not specified, it is name<br>
type - data types: str, int (string and number)<br>
default - you can specify a default value<br>
Create cache field, to create a unique field - name="cache" - creates a cache-string by the value of the field cache_field<br>

Example:<br>
<tablefields><br>
<field name="title" property_name="title"></field><br>
<field name="url_post" property_name="url_post"></field><br>
<field name="date" property_name="date"></field><br>
<field name="avtor" property_name="avtor"></field><br>
<field name="published" property_name="" default="0" type="int"></field><br>
<field name="cashe" property_name="" cashe_field="title"></field><br>
</tablefields><br>

Then there are fields to set the spider:<br>
- <encoding></encoding> - you can specify the encoding, default utf-8<br>
- <agent></agent> - description of spider agent properties, default: Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0<br>

Further there are fields to set the spider crawling pages:
- <selector>article.post_preview</selector> - selector for selecting information blocks from which data will be extracted<br>
- <nextselector></nextselector> - selector to find the next page<br>
- <maxpage>2</maxpage> - the maximum number of pages to becrawling is 1 by default, if 0 is specified, it will attempt to crawling all<br>
- <nextpage>https://habr.com/ru/all/page</nextpage> - the basis for generating the address of the next page with a usage counter:<br>
next_page = nextpage + str(counter) - https://habr.com/ru/all/page1, https://habr.com/ru/all/page2 и тд.<br>
- <endselector></endselector> - stop selector, if it is found on the page, the spider will stop

For example glamour.xml:<br>
<selector>ul.c-card-section__card-list li</selector><br>
<maxpage>0</maxpage><br>
<nextpage></nextpage><br>
<nextselector></nextselector><br>
<endselector></endselector><br>
Since it is not specified how to proceed, the spider crawling only the starting address.<br>

Then the section begins <properties></properties> - description of data properties and how to get them from the information block selector.<br>
The data field is described in the section <property></property> as follows, for example habr.xml:<br>
<property><br>
<name>title</name> - the name of the property<br>
<before></before> - you can insert text before the data value<br>
<selector>h2.post__title a::text</selector> - data selection selector - it may be absent. If it is equal to Now, - that value will become equal to the current date in the format %d-%m-%Y<br>
<after></after> - you can insert text that follows the data value<br>
<replace_filters></replace_filters> - filter section, can be empty<br>
</property><br>

Аilter section <replace_filters></replace_filters>, consists of sections:<br>
<filter><old>old_value</old><new>new_value</new></filter> - where it is specified what data in value will be replaced and on what<br>

For example glamour.xml:<br>
<property><br>
<name>url_img</name><br>
<before></before><br>
<selector>div.c-card__image noscript</selector><br>
<after></after><br>
<replace_filters><br>
<filter><old>noscript</old><new></new></filter> - delete noscript(value <old>noscript</old>) from data value text<br>
<filter><old>&gt;</old><new></new></filter> - delete &gt;(value <old>&gt;</old>) from data value text<br>
<filter><old>&quot;</old><new>"</new></filter> - replace &quot;(value <old>&quot;</old>) on " (value <new>"</new>) in data value text<br>
</replace_filters><br>
</property><br>

For example glamour.xml:<br>
<property><br>
<name>site</name><br>
<before>www.glamourmagazine.co.uk</before><br>
<selector></selector><br>
<after></after><br>
<replace_filters></replace_filters><br>
</property><br>
Value property - site - will be equal www.glamourmagazine.co.uk<br>

<property><br>
<name>date</name><br>
<before></before><br>
<selector>Now</selector><br>
<after></after><br>
<replace_filters></replace_filters><br>
</property><br>
Value property - date - will be equal to the current date in the format %d-%m-%Y

