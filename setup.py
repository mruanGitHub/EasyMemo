# useage: python setup.py py2exe
from distutils.core import setup
import py2exe
from glob import glob
# copy dll

#data_files = [("Microsoft.VC90.CRT", glob(r'c:\dev\ms-vc-runtime\*.*')),
#              (".", ["SmallEditor.ico","Diary.exe"])
#              ]

data_files = [(".", ["SmallEditor.ico","Diary.exe", "msvcp90.dll", "diary.txt"])]
setup( 
       name = "SmallEditor (Unicode)",
       version = "1.0",
       author = "Ming Ruan",
       author_email = "ming.ruan@yahoo.com",
       url = "http://www.yahoo.com",
       #console=['SmallEditor.py'],
       windows=['SmallEditor.py'],
       data_files=data_files
     )
