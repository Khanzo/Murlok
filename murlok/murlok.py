# -*- coding: utf-8 -*-
import os
import hashlib
import xml.etree.ElementTree as ET
from string import Template

class Field:
    #<field name="published" property_name="" default="1" type="int"></field>
    def __init__(self,_field_name, _property_name, _default="", _field_type="str", cashe_field=""):
        self.name = _field_name
        self.property = _property_name
        self.default = _default
        self.type = _field_type
        self.cashe_field = cashe_field

class Filter:
    #<filter><old></old><new></new></filter>
    def __init__(self,_old, _new):
        self.old = _old
        self.new = _new

class Property:
    """
    <property>
    <name></name>
    <before></before>
    <selector></selector>
    <after></after>
    <replace_filters>
    <filter><old></old><new></new></filter>
    </replace_filters>
    </property>
    """

    def init_filters(self, filters):
        if len(filters)>0:
            for key, val in filters.items():
                self.filters.append(Filter(key,val))


    def __init__(self, _title, _before, _selector, _after, _filters):
        self.title = _title
        self.before = _before
        self.selector = _selector
        self.after = _after
        self.filters = _filters
        #self.init_filters(_filters)

class Murlok():

    def isNone(self,text,default=''):
        if text is None:
            return default
        else:
            return text

    def isAttr(self,node,attr_name,default=''):
        if attr_name in node.attrib:
            return node.attrib[attr_name]
        else:
            if self.format == "mysql" and attr_name == "port":
                default = "3316"
            if self.format == "postg" and attr_name == "port":
                default = "5432"
            return default

    def dictfields(self, node):
        _fields = dict()
        if node is None:
            #defaults  field.title = prop.title
            for prop in self.murlok.properties:
                field = Field(prop.title,prop.title)
                _fields[prop.title] = field
        else:
            for f in node.findall('field'):
                field_name = self.isAttr(f,'name')
                property_name = self.isAttr(f,'property_name')
                
                if len(property_name) == 0:
                    property_name = field_name
                    
                default = self.isAttr(f,'default','')
                _type =self.isAttr(f,'type','str')
                cashe_field = self.isAttr(f,'cashe_field','')
                field = Field(field_name,property_name,default,_type,cashe_field)
                _fields[property_name] = field
        return _fields

    def generatesql(self):
        if self.format == "sqlite":
            sql_table = "INSERT OR IGNORE INTO `" + self.table + "` "
        else:
            sql_table = "INSERT IGNORE INTO `" + self.table + "` "
        sql_columns = "("
        sql_value = "("
        for key,val in self.fields.items():
            sql_columns = sql_columns + "`" + val.name + "`"

            if val.type == "str":
                sql_value = sql_value + '"$' + key + '"'
            else:
                sql_value = sql_value + '$' + key

            sql_columns = sql_columns + ','
            sql_value = sql_value + ','
        sql_columns = sql_columns[:-1] + ')'
        sql_value = sql_value[:-1] + ')'
        return Template(sql_table + sql_columns + ' VALUES ' + sql_value)

    def cashed(self,value):
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    def getDict(self,d):
        l = self.fields.keys() - d.keys()

        for lkey in l:
            d[lkey] = self.fields[lkey].default
            if lkey == 'cashe':
                cashe_column = self.fields[lkey].cashe_field
                d[lkey] = self.cashed(d[cashe_column])

        return d


    def readconfig(self, xml_config):
        spec = ['&quot;','&apos;','&lt;','&gt;','&amp;']
        symbol = ['"',"'",'<','>','&']
        formats = ('mysql', 'postg', 'sqlite')

        tree = ET.parse(xml_config)
        root = tree.getroot()

        self.spider = self.isNone(root.find('name').text,'murlok')
        self.start = self.isNone(root.find('start_url').text)
        self.selector = self.isNone(root.find('selector').text)
        self.endselector = self.isNone(root.find('endselector').text)
        self.format = self.isNone(root.find('format').text,'json')

        if self.format in formats:
            connect = root.find('peewee')
            if connect is not None:
                self.db = self.isAttr(connect,'db')
                self.host = self.isAttr(connect,'host','localhost')
                self.user = self.isAttr(connect,'user')
                self.passw = self.isAttr(connect,'pass')
                self.port = self.isAttr(connect,'port')
                self.charset = self.isAttr(connect,'charset')
                self.table = self.isAttr(connect,'table')
                table_field = connect.find('tablefields')
                self.fields = self.dictfields(table_field)

        self.agent = self.isNone(root.find('agent').text,'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0')
        self.encoding = self.isNone(root.find('encoding').text,'utf-8')

        if root.find('maxpage').text is None:
            self.maxpage = 1
        else:
            self.maxpage = int(root.find('maxpage').text)

        self.nextselector = self.isNone(root.find('nextselector').text)
        self.nextpage = self.isNone(root.find('nextpage').text)

        for item in root.find('properties').findall('property'):
            title = self.isNone(item.find('name').text)
            before = self.isNone(item.find('before').text)
            selector = self.isNone(item.find('selector').text)
            after = self.isNone(item.find('after').text)

            replace_filters = item.find('replace_filters').findall('filter')
            filters = dict()

            if len(replace_filters) >0:
                for filt in replace_filters:
                    old_filt = self.isNone(filt.find('old').text)
                    new_filt = self.isNone(filt.find('new').text)

                    for i in range(5):
                        old_filt = old_filt.replace(spec[i],symbol[i])
                        new_filt = new_filt.replace(spec[i],symbol[i])
                    filters[old_filt] = new_filt
            prop = Property(title, before, selector, after, filters)
            self.properties.append(prop)

    def findprop(self,_title):
        prop = None

        for _prop in self.properties:
            if _title == _prop.title:
                prop = _prop
                break;
        return prop

    def filtertext(self, _title, _text):
        filttext = _text.replace('\n','').replace('\t','')
        prop = self.findprop(_title)

        if prop is None:
            return filttext

        if len(prop.filters)>0:
            for key, val in prop.filters.items():
                filttext = filttext.replace(key,val)
        return filttext


    def __init__(self, xml_config):
        self.config = xml_config
        self.spider = 'murlok'
        self.start = ''
        self.nextselector = ''
        self.nextpage = ''
        self.maxpage = 1
        self.format = 'json'
        self.agent = ''
        self.encoding = 'utf-8'
        self.selector = ''
        self.endselector = ''
        self.properties = []

        self.db = ""
        self.host = "localhost"
        self.user = ""
        self.passw = ""
        self.port = ""
        self.charset = ""
        self.table = ""
        self.fields = dict()

        if os.path.exists(xml_config):
            self.readconfig(xml_config)