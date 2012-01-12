'''
Created on Nov 16, 2011

@author: Daniel Kershaw
'''
import AlchemyAPI as API
from xml.etree import ElementTree as ET
from Crawler import Crawler
class GetData(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.Alchemy = API.AlchemyAPI()
        self.Alchemy.loadAPIKey("./AlchemyAPI.txt")
        
    def getWebPage(self, url, depth):
        if int(depth) != 0:
            t = ""
            crawler = Crawler(url, int(depth)-1)
            crawler.crawl()
            for l in crawler.links_remembered:
                print 'Sending AlchemyAPI request for: ' + str(l.dst)
                text = self.Alchemy.URLGetText(str(l.dst))     
                element = ET.XML(text)
                t += element.findtext("text")
            print 'This is all the text: '+ t
        else:
            text = self.Alchemy.URLGetText(url)     
            element = ET.XML(text)
            t = element.findtext("text")
        print type(t)
        return t.encode('ascii','ignore')
    
    def getPageTitle(self, url):
        text = self.Alchemy.URLGetTitle(url)
        element = ET.XML(text)
        t = element.findtext("title")
        return t.decode('utf8','ignore')
