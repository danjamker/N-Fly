'''
Created on Nov 16, 2011
This is on the windows mechine
@author: Daniel Kershaw
'''
from cgi import parse_qs, escape
from cherrypy import wsgiserver
from run import runable
import json
import os
import re
import time

def application(environ, start_response):
    print 'Incoming'
    d = parse_qs(environ['QUERY_STRING'])
    
    if re.match('^http\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)?$' , d.get('url',[''])[0]) != None:
        if d.get('depth',[''])[0].isdigit() == True:
            url = d.get('url',[''])[0]
            depth = d.get('depth',[''])[0]
            
            url = escape(url)
            depth = escape(depth)
            
            #Used to time the function
            t_start = time.time()     
            results = R.run(url, depth)
            t_end = time.time()
            
            tmp = [{'depth':depth, 'time':time.time(), 'run time':((t_end-t_start)*1000.0), 'src_url':url, 'keywords':results}]
            response_text = json.dumps(tmp)
            
            print 'This query took %0.3f ms' % ((t_end-t_start)*1000.0)
                                     
            status = '200 OK'
        else:
            status = '200 OK'
            response_text = "usage:?url=<url>&depth=<int on depth>"           
    else:
        status = '200 OK'
        response_text = "usage:?url=<url>&depth=<int on depth>"
        
    response_headers = [('Content-Type', 'application/json'), ('Content-Length', str(len(response_text)))]

    start_response(status, response_headers)
    
    return [response_text.encode('UTF-8', 'replace')]

if __name__ == '__main__':
    #Set up proxy for university network and set working directory
    os.environ["http_proxy"] = "http://wwwcache.lancs.ac.uk:8080"
    os.chdir('.')
    
    R = runable()
    
    #Indicate when server is starting
    print os.getcwd()
    httpd = wsgiserver.CherryPyWSGIServer(
            ('0.0.0.0', int(os.environ.get('PORT', '5000'))), application,
            server_name='www.cherrypy.example')
    httpd.start()
    
