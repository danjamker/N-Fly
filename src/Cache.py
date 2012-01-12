'''
Created on Dec 5, 2011

@author: Daniel Kershaw
'''
import MySQLdb as MySQL
import sys
import time 

class Cache(object):
    '''
    classdocs
    '''

    db = None
    cur = None
    
    def __init__(self):
        '''
        Constructor
        '''
        try:
            db = MySQL.Connect("localhost", "root", "173wgpiK", "cache")
            cur = db.cursor()
            
        except MySQL.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
        
    def check(self, url):
        cur.execute("SELECT * FROM webpage WHERE webpage.URL = " + url)
        data = cur.fetchone()
        
        if data == None:
            return 0, None
        else:
            ttl = int(data[3])
            lit = int(data[2])
            
            if (lit < (lit + ttl)):
                cur.execute("SELECT keyword FROM keyword WHERE keyword.idwebpage = " + str(data[0]))
                keywords = cur.fetchall()
                tmp = []
                for words in keywords:
                    tmp.append(words[1])
                return 1, tmp
            else:
                #Needs to be reindexed
                return 2, None
            
    def input(self, url, keywords, ttl = 15):
        cur.execute("SELECT * FROM webpage WHERE webpage.URL = " + url)
        data = cur.fetchone()

        if data == None:
            cur.execute("INSERT INTO `cache`.`webpage` (`URL`, `lasted_index`, `time_of_life`) VALUES ("+url+", "+str(time.time())+","+str(ttl*60)+" )")
            cur.execute("SELECT idwebpage FROM webpage WHERE webpage.url =" + url)
            data = cur.fetchone()
            
            for word in keywords:
                cur.execute("INSERT INTO `cache`.`keyword` (`keyword`, `idwebpage`) VALUES ("+word+","+str(data[0])+")")
        else:
            cur.execute("UPDATE `cache`.`webpage` SET `lasted_index`="+str(time.time()))+", `time_of_life`="+str(ttl)+" WHERE `idwebpage`="+str(data[0]))
            cur.execute("DELETE FROM keyword WHERE idwebpage = " + str(data[0])))  
            
            for word in keywords:
                cur.execute("INSERT INTO `cache`.`keyword` (`keyword`, `idwebpage`) VALUES ("+word+","+str(data[0])+")")
        
        return None