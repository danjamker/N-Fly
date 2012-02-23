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
        
    print "Prossision:"
    print p
    return p

def recall(human, computer):
    
    a = len(set(human)&set(computer))
    c = len(set(human)-(set(human)&set(computer)))
    
    try:
        r = float(a) /(float(a)+float(c))
    except:
        r = 0

    print "Recall:"
    print r
    return r

def fscore(human, computer):
    
    p = precision(human, computer)
    r = recall(human, computer)
    
    try:
        f = float((2*p*r)/(p+r))
    except:
        f = 0
        
    print "f-messure:"
    print f    
    return f

if __name__ == '__main__':
    getcontext().prec = 50
    try:
        db = MySQL.Connect("localhost", "root", "root", "evaluation")
        cur = db.cursor()
        
        cur.execute("SELECT * FROM evaluation.setup")

        data = cur.fetchall()
        

        
        for setup in data:
            setupstring = setup[1]
            setupstring = setupstring.split(' ')
            llwl_tmp = None
            percen_tmp = None
            NE_tmp = False
            Col_tmp = False
            Gram_tmp = False
            Chu_tmp = False
            for settings in setupstring:
                if settings == '-c':
                    Col_tmp = True
                elif settings == '-ch':
                    Chu_tmp = True
                elif settings == '-ne':
                    NE_tmp = True
                elif settings == '-gra':
                    Gram_tmp = True
                elif settings == '-AmE06':
                    llwl_tmp = 'AmE06'
                elif settings == '-BE06':
                    llwl_tmp = 'BE06'
                elif settings == '-Brown':
                    llwl_tmp = 'Brown'
                elif settings == '-p(20)':
                    percen_tmp = 20
                elif settings == '-p(40)':
                    percen_tmp = 40
                elif settings == '-p(60)':
                    percen_tmp = 60
                elif settings == '-p(80)':
                    percen_tmp = 80
                elif settings == '-p(100)':
                    percen_tmp = 100
            s = Nfly( llwl = llwl_tmp, percen = percen_tmp, NE = NE_tmp, Col = Col_tmp, Gram = Gram_tmp, Chu = Chu_tmp) #This is where the setup will go
            
            cur.execute("INSERT INTO `evaluation`.`test` (`date`, `idsetup`) VALUES (NOW(), "+str(setup[0])+")")
            cur.execute("SELECT * FROM test ORDER BY idtest DESC LIMIT 1")
            test = cur.fetchone()
            
                      
            cur.execute("SELECT * FROM webpage")
            datawp = cur.fetchall()
            
            print 'Complete Webpage test set: ', datawp
            
            for page in datawp:
                
                t_start = time.time()     
                keywords = s.run(page[1], 0)
                print "The Keywords are: ", keywords
                t_end = time.time()
                                
                cur.execute("SELECT keyword FROM keyword WHERE keyword.idwebpage =" + str(page[0]))
                kw = cur.fetchall()
                tmp = []
                for word in kw:
                    tmp.append(word[0])
                    
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

