===============
Project N-Fly
===============
This is my Final Year Project at Lancaster University. 

:Authors:
    Daniel Kershaw
:Version: 0.1 of 26/01/2011 

---------------
Install - UNIX
---------------
To run the system first run the install script, ./install.sh as this will install all needed dependencies of the code. This is for UNIX only. 

>>> ./install.sh

Once installed run Python command line following the instructions to download all the data from the NLTK servers. 

>>> import nltk
nltk.download()
...

---------------
Install - Win32
---------------
You will need to obtain the following packages and install them on your computer using an administrator account:

- Python: http://www.python.org/ftp/python/2.6.6/python-2.6.6.msi
- PyYAML: http://pyyaml.org/download/pyyaml/PyYAML-3.09.win32-py2.6.exe
- NLTK: http://nltk.googlecode.com/files/nltk-2.0b9.win32.msi
- Numpy: http://prdownloads.sourceforge.net/numpy/numpy-1.5.1-win32-superpack-python2.6.exe
- Matplotlib: http://prdownloads.sourceforge.net/matplotlib/matplotlib-1.0.1.win32-py2.6.exe (it is sometimes necessary to download an extra DLL http://www.dll-files.com/dllindex/dll-files.shtml?msvcp71, to C:\WINDOWS\system32\)
- CherryPi: http://download.cherrypy.org/cherrypy/3.2.2/CherryPy-3.2.2.win32.exe

Once installed run Python command line following the instructions to download all the data from the NLTK servers. 

>>> import nltk
nltk.download()
...

---------------
Run
---------------
Navigate to root source code directory, and depending on the system run the command bellow. 

- UNIX: 

>>> python ./main/main.py

- Windows:

>>> ./main/main.py
 
---------------
External Links
---------------
- `Python <http://www.python.org/>`_
- `NLTK <http://www.nltk.org>`_
- `NumPy <http://numpy.scipy.org/>`_
- `CherryPy <http://cherrypy.org/>`_

---------------
Copyright 
---------------
All copy right over the code is held by (Daniel Kershaw), unless stated other wise stated.

AmE06 and BE06 are held by Lancaster University. 