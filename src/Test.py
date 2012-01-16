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
    
    try:
        p = float(a) /(float(a)+float(b))
    except:
        p = 0
        

    return p

def recall(human, computer):
    
    a = len(set(human)&set(computer))
    c = len(set(human)-(set(human)&set(computer)))
    
    try:
        r = float(a) /(float(a)+float(c))
    except:
        r = 0

    return r

def fscore(human, computer):
    
    p = precision(human, computer)
    r = recall(human, computer)
    
    try:
        f = float((2*p*r)/(p+r))
    except:
        f = 0
        
    return f

if __name__ == '__main__':
    getcontext().prec = 50
    try:
        db = MySQL.Connect("localhost", "root", "root", "evaluation")
        cur = db.cursor()
        
        cur.execute("SELECT * FROM evaluation.setup")

        data = cur.fetchall()
        
        s = Nfly() #This is where the setup will go

        
        for setup in data:
            cur.execute("INSERT INTO `evaluation`.`test` (`date`, `idsetup`) VALUES (NOW(), "+str(setup[0])+")")
            cur.execute("SELECT * FROM test ORDER BY idtest DESC LIMIT 1")
            test = cur.fetchone()
            
                      
            cur.execute("SELECT * FROM webpage")
            datawp = cur.fetchall()
            
            print 'Complete Webpage test set: ', datawp
            
            for page in datawp:
                
                t_start = time.time()     
                #keywords = ['ex', 'am', 'apple']
                keywords = s.run(page[1], 0)
                print "The Keywords are: ", keywords
                t_end = time.time()
                                
                cur.execute("SELECT keyword FROM keyword WHERE keyword.idwebpage =" + str(page[0]))
                kw = cur.fetchall()
                kw = ['daniel','emma','apple']
                tmp = []
                for word in kw:
                    tmp.append(word[1])
                    
                p = precision(keywords, tmp)
                r = recall(keywords, tmp)
                f = fscore(keywords, tmp)
                
                t_diffrence = t_end-t_start
                sql = "INSERT INTO `evaluation`.`test_webpage` (`runtime`, `idwebpage`, `idtest`, `prosision`, `fmeasure`, `recall`, `date`) VALUES (%s ,%s ,%s ,%s ,%s ,%s , NOW())" % (t_diffrence,page[0],test[0],p,f,r,)
                cur.execute(sql)
                cur.execute("SELECT * FROM test_webpage ORDER BY idtest DESC LIMIT 1")
                test_webpage = cur.fetchone()
                
                for word in keywords:
                    sql = "INSERT INTO `evaluation`.`test_keyword` (`keyword`, `idwebpage`) VALUES ('"+word+"',"+str(test_webpage[0])+")"
                    cur.execute(sql)

                
    except MySQL.Error, e:
    
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
        
    finally:
    
        if db:
            db.commit() 
            db.close()
            
    pass

