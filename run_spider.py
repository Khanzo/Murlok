# -*- coding: utf-8 -*-
import sys
import os
from murlok.spiders.murlokspider import MurlokSpider
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging   
from scrapy.utils.project import get_project_settings         
from murlok.murlok import Murlok

#python run_spider.py habr.xml

def main():
    if len(sys.argv) != 2:
        print('usage: run_spider.py file-config')
        sys.exit(1)
    file_config = sys.argv[1]
    if not os.path.exists(file_config):
        print(f'Not found: {file_config}')
        sys.exit(1)
    
    configure_logging()
    settings = get_project_settings()
    
    _murlok = Murlok(file_config)
    
    formats = ('json', 'xml', 'jsonlines', 'csv', 'pickle', 'marshal')    
    settings.overrides['FEED_EXPORT_ENCODING'] = str(_murlok.encoding)    
    if _murlok.format in formats:
        settings.overrides['FEED_FORMAT'] = str(_murlok.format)
        settings.overrides['FEED_URI'] = str(_murlok.spider) + '.' + str(_murlok.format)
        settings.overrides['ITEM_PIPELINES']='{"murlok.pipelines.MurlokPipeline": 300}'
    else:
        #Pippeline config peewee - pip install -U peewee
        settings.overrides['ITEM_PIPELINES']='{"murlok.pipelines.MurlokPipeline": 300}'
        pass
    
    runner = CrawlerProcess(settings)
    runner.crawl(MurlokSpider,murlok = _murlok)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
    
if __name__ == '__main__':
    main()