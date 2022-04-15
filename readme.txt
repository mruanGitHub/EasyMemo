-- Today is 15-04-2022

----------------------------------------------------------------------------------
This SmallEditor is developed using Python/wxPython/AutoHotKey, packed using NSIS
For bugs or other issues please contact me: ming_ruan@yahoo.com

My LinkedIn profile:  http://nl.linkedin.com/pub/mingchuan-ruan/66/34a/16b
----------------------------------------------------------------------------------

Usage:
- Install SmallEditor in e.g. C:\SmallEditor\
- Start SmallEditor by double click the icoon 'SmallEditor'
- Then you may use Ctrl+E to load the 'diary.txt'
- Ctrl+M will load a small AHK program which will let you input texts
- Your texts will be automatically saved in the 'diary.txt'

For developers (only):

- Install python2.7 (python-2.7.14.msi)
- Install py2exe (choose 32 or 64 bit)
- Install wxPython Unicode! (choose 32 or 64 bit)

(Don't use: pip install -U wxPython, because it will install a higer version 4.0 but not Unicode compatible!)
(If necessary, to uninstall: pip uninstall wxPython)

- Install NSIS (nsis-3.03-setup.exe)

- Run make.bat, which will create two folders: ./build/ and ./dist/

- SmallEditor.nsi is the script for creating the installer (right click the file and Compile NSIS Script)
