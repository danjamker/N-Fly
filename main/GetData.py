'''
Created on Nov 16, 2011

@author: Daniel Kershaw

Modual for the access of cleaned data for the N-Fly system.
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
        Selects and returns all data to a depth indicated.
        
        @param URL: URL which is going to be the sourse
        @param depth: the depth of the links from the URL which should be searched
        
        @return: a String will the the text concatonated. 
        '''
        page = self.getWebPage(URL, depth)
        title = self.getPageTitle(URL) 
        return title + page
        
    def getWebPage(self, URL, depth):
        '''
        Retreve all the text data from webpage/webpages.
        
        @param URL: URL which is going to be the sourse
        @param depth: the depth of the links from the URL which should be searched
        default = 0
        
        @return: string of all text from all webpages. 
        '''
        if int(depth) != 0:
            t = ""
            crawler = Crawler(URL, int(depth)-1)
            crawler.crawl()
            for l in crawler.links_remembered:
                text = self.Alchemy.URLGetText(str(l.dst))     
                element = ET.XML(text)
                t += element.findtext("text")
        else:
            text = self.Alchemy.URLGetText(URL)     
            element = ET.XML(text)
            t = element.findtext("text")
        return t.encode('ascii','ignore')
    
    def getPageTitle(self, URL):
        '''
        Method for retriving the file name of the webpage.
        
        @param URL: URL which is page to get title from
        @return: the title of the webpage.        
        '''
        text = self.Alchemy.URLGetTitle(URL)
        element = ET.XML(text)
        t = element.findtext("title")
        return t.decode('ascii','ignore')
