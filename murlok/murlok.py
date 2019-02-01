# -*- coding: utf-8 -*-
import os
import xml.etree.ElementTree as ET

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
    
    def readconfig(self, xml_config):
        spec = ['&quot;','&apos;','&lt;','&gt;','&amp;']
        symbol = ['"',"'",'<','>','&']
        
        tree = ET.parse(xml_config)
        root = tree.getroot()
        
        self.spider = self.isNone(root.find('name').text,'murlok')            
        self.start = self.isNone(root.find('start_url').text)            
        self.selector = self.isNone(root.find('selector').text)    
        self.endselector = self.isNone(root.find('endselector').text) 
        self.format = self.isNone(root.find('format').text,'json')        
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
        self.dbconfig = dict()
        if os.path.exists(xml_config): 
            self.readconfig(xml_config) 