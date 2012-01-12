'''
Created on Nov 30, 2011

@author: Daniel Kershaw
'''
import MySQLdb as MySQL
from run import runable as Nfly
import sys
import time
from decimal import *

db = None

def precision(human, computer):
    
    a = len(set(human)&set(computer))
    b = len(set(computer)-(set(human)&set(computer)))
    
    p = float(a) /(float(a)+float(b))

    return p
    
def recall(human, computer):
    
    a = len(set(human)&set(computer))
    c = len(set(human)-(set(human)&set(computer)))

    r = float(a) /(float(a)+float(c))

    return r

def fscore(human, computer):
    
    p = precision(human, computer)
    r = recall(human, computer)
    
    f = float((2*p*r)/(p+r))
    
    return f

if __name__ == '__main__':
    getcontext().prec = 50
    try:
        db = MySQL.Connect("localhost", "root", "173wgpiK", "evaluation")
        cur = db.cursor()
        
        cur.execute("SELECT * FROM setup")

        data = cur.fetchall()
        

        
        for setup in data:
            #s = Nfly() #This is where the setup will go
            cur.execute("INSERT INTO `evaluation`.`test` (`date`, `idsetup`) VALUES (NOW(), "+data[0]+")")
            cur.execute("SELECT len(*) FROM test")
            test = cur.fetchone()  
                      
            cur.execute("SELECT * FROM webpage")
            datawp = cur.fetchall()
            
            for page in datawp:
                print page
                
                t_start = time.time()     
                keywords = ['ex', 'am', 'apple']
                #keywords = s.run(page[0], 0)
                t_end = time.time()
                                
                cur.execute("SELECT keyword FROM keyword WHERE keyword.idwebpage =" + str(page[0]))
                kw = cur.fetchall()

                tmp = []
                for word in kw:
                    tmp.append(word[0])
                    
                p = precision(keywords, tmp)
                r = recall(keywords, tmp)
                f = fscore(keywords, tmp)
                
                cur.execute("INSERT INTO `evaluation`.`test_webpage` (`runtime`, `idwebpage`, `idtest`, `prosision`, `fmeasure`, `recall`, `date`) VALUES ("+str(t_end-t_start)+", "+str(page[0])+", "+str(test[0])+", "+str(p)+", "+str(f)+", "+str(r)+", NOW())")
                cur.execute("SELECT len(*) FROM test_webpage")
                test_webpage = cur.fetchone()
                
                for word in tmp:
                    cur.execute("INSERT INTO `evaluation`.`test_keyword` (`keyword`, `idwebpage`) VALUES ("+word+","+str(test_webpage[0])+")")

                
    except MySQL.Error, e:
    
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
        
    finally:
    
        if db:
            db.close()
            
    pass

