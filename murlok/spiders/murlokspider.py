# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.exceptions import CloseSpider

class MurlokSpider(scrapy.Spider):    
    
    def __init__(self, *args, **kw):
        self.murlok = kw.get('murlok')
        self.start_urls = [self.murlok.start] 
        self.name = self.murlok.spider
        self.counter = 1        
        
    def start_requestss(self):        
        for url in self.start_urls:            
            yield scrapy.Request(url, headers={"User-Agent':'"+str(self.agent)+"'"})
        
    def parse(self, response):
        
        if self.murlok.selector == '':
            raise CloseSpider('Stop crawl')
            
        for row in response.css(self.murlok.selector):
            item = {} 
            date = datetime.date.today()
            date_str = date.strftime("%d-%m-%Y") 
            for prop in self.murlok.properties: 
                if len(prop.selector) == 0:
                    item[prop.title] = prop.before + ''+ prop.after
                    continue
                if prop.selector == 'Now':
                    item[prop.title] = date_str
                    continue                
                str_result = row.css(prop.selector).extract_first()
                if str_result is None:
                    str_result = ''                
                str_result = self.murlok.filtertext(prop.title,str_result)
                item[prop.title] = prop.before + str_result + prop.after                                  
            yield item
        
        if self.murlok.maxpage >0:
            self.counter = self.counter + 1
            if self.counter > self.murlok.maxpage:
                raise CloseSpider('Stop crawl')
                
        if len(self.murlok.endselector)>0:
            endselector = response.css(self.murlok.endselector).extract_first()
            if endselector is not None and len(endselector)>0:
                raise CloseSpider('Stop crawl')
                
        next_page = ''
        
        if len(self.murlok.nextselector)>0: 
            next_page = response.css(self.murlok.nextselector).extract_first()
        else:
            if len(self.murlok.nextpage)>0:
                next_page = self.murlok.nextpage + str(self.counter)
                
        if next_page is not None and len(next_page)>0:
            yield response.follow(next_page, self.parse)