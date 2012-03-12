'''
Created on Nov 16, 2011

@author: Daniel Kershaw
'''
import AlchemyAPI as API
from xml.etree import ElementTree as ET
from Crawler import Crawler
class GetData(object):
    '''
    Class for retreving the strip data from webpages. 
    '''


    def __init__(self):
        '''
        Inisiates the AlchemyAPI class, and SDK
        '''
        self.Alchemy = API.AlchemyAPI()
        self.Alchemy.loadAPIKey("./AlchemyAPI.txt")
        
    def getData(self, URL, depth = 0):
        '''
        @param URL: URL which is going to be the sourse
        @param depth: the depth of the links from the URL which should be searched
        default = 0
        
        @return: a String will the the text concatonated. 
        '''
        page = self.getWebPage(URL, depth)
        title = self.getPageTitle(URL) 
        return title + page
        
    def getWebPage(self, url, depth):
        '''
        Retreve all the text data from webpage/webpages.
        
        @param URL: URL which is going to be the sourse
        @param depth: the depth of the links from the URL which should be searched
        default = 0
        
        @return: string of all text from all webpages. 
        '''
        if int(depth) != 0:
            t = ""
            crawler = Crawler(url, int(depth)-1)
            crawler.crawl()
            for l in crawler.links_remembered:
                text = self.Alchemy.URLGetText(str(l.dst))     
                element = ET.XML(text)
                t += element.findtext("text")
        else:
            text = self.Alchemy.URLGetText(url)     
            element = ET.XML(text)
            t = element.findtext("text")
        return t.encode('ascii','ignore')
    
    def getPageTitle(self, url):
        '''
        Method for retriving the file name of the webpage.
        
        @param URL: URL which is page to get title from
        @return: the title of the webpage.        
        '''
        text = self.Alchemy.URLGetTitle(url)
        element = ET.XML(text)
        t = element.findtext("title")
        return t.decode('ascii','ignore')
