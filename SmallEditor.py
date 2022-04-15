"""
SmallEditor (Unicode compatible!): Use wxPython/AHK, Py2exe and NSIS
A Small test wxPython program along with py2Exe scripts to build a windows executable
(Ming, originally on 05 March 2010; imporved in 2012)
To do's:
    1. if NO-BREAK spaces (hex A0) in the text encounterd, it will only show blank!
Done!:
    1. Added 'Save as' file exists 27/09/12
    2. Added Tool menuBar 27/09/12
    3. Added Open With (exteral argument) 30/09/12
    4. Fix bug in 'Save as' 30/09/12
"""
#import pycallgraph
#pycallgraph.start_trace()

import os
import sys
#import win32_unicode_argv # for unicode argv
import subprocess
import time
# don't use xyPython because it is deprecated use wx instead
#from wx.Python.wx import *
import wx
#from wx.tools.XRCed import images  #This doesn't work. I have to copy images to the working Dir.
import images
#
from Printer import Printer

# test Unicode
# Some unicode strings

chi_uni = (u'Python \u662f\u6700\u597d\u7684\u7de8\u7a0b\u8a9e\u8a00\uff01',
            'Python is the best\nprogramming language!')
#-------------------------------------------------------------------------------
# Define booleans until Python ver 2.7
True=1
False=0

APP_NAME = "SmallEditor V1.2"

# --- Menu and control ID's
#ID_NEW=101
#ID_OPEN=102
#ID_SAVE=103
#ID_SAVEAS=104
#ID_EXIT=109
#ID_FIND =121
#ID_ABOUT=141
ID_RTB=201

SB_INFO = 0
SB_ROWCOL = 1
SB_DATETIME = 2

# --- our frame class
class smallAppFrame(wx.Frame):
    """ Derive a new class of wx.Frame. """
    overviewText = "wxPython Overview"

    def __init__(self, parent, id, title):
        # --- a basic window frame/form
        wx.Frame.__init__(self, parent = None, id = -1,
			title = APP_NAME + " - Developed in wxPython/AHK",
                         pos = wx.Point(0, 0), size = wx.Size(640, 480),
                         name = '', style = wx.DEFAULT_FRAME_STYLE)
                        
        if(len(sys.argv)) == 2:
            self.Bind(wx.EVT_ACTIVATE,  self.OnFileOpenDirect)
         #   wx.EVT_ACTIVATE(self,  self.OnFileOpenDirect)  # same

        self.printer = Printer(self)
        self.SetMinSize((640,480))
        # --- real windows programs have icons, so here's ours!
        try:# - don't sweat it if it doesn't load
            self.SetIcon(wx.Icon("SmallEditor.ico", wx.BITMAP_TYPE_ICO))
        finally:
            pass

        self.codePage = None
        self.finddlg = None

        # --- add a menu, first build the menus (with accelerators)
        self.BuildMenuBar()
        
        self.finddata = wx.FindReplaceData()
        self.finddata.SetFlags(wx.FR_DOWN)
        #  Not needed!, just put them in text form after tab in menu item!
        # --- add accelerators to the menus
        #self.SetAcceleratorTable(wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('O'), ID_OPEN), 
        #                          (wx.ACCEL_ALT, ord('Q'), ID_EXIT)]))

        # --- add a statusBar (with date/time panel)
        sb = self.CreateStatusBar(3)
        sb.SetStatusWidths([-1, 65, 160])
        sb.PushStatusText("Ready", SB_INFO)
        # --- set up a timer to update the date/time (every 5 seconds)
        self.timer = wx.PyTimer(self.Notify)
        self.timer.Start(5000)
        self.Notify()       # - call it once right away

        # --- add a control (a RichTextBox) & trap KEY_DOWN event
        self.rtb = wx.TextCtrl(self, ID_RTB, size=wx.Size(400*2,200*2),
                              style=wx.TE_MULTILINE | wx.TE_RICH2)
        ### - NOTE: binds to the control itself!
        wx.EVT_KEY_UP(self.rtb, self.OnRtbKeyUp)

        # --- need to add a sizer for the control - yuck!
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        # self.sizer.SetMinSize(200,400)
        self.sizer.Add(self.rtb, 1, wx.EXPAND)
        # --- now add it to the frame (at least this auto-sizes the control!)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
        self.sizer.SetSizeHints(self)

        # Add some Unicode (Chinese!)
        if not wx.USE_UNICODE:
            self.AddLine(self.sizer)
            self.AddText(self.sizer, "Sorry, this wxPython was not built with Unicode support.",
                    font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD) )
            self.AddLine(self.sizer)
        else:
            f = self.GetFont()
            font = wx.Font(14, f.GetFamily(), f.GetStyle(), wx.BOLD, False,
                          f.GetFaceName(), f.GetEncoding())
            self.AddLine(self.sizer)
            self.AddText(self.sizer, chi_uni[0], chi_uni[1], 'Chinese:', font)
            self.AddLine(self.sizer) 

        # --- initialize other settings
        self.dirName = ""
        self.fileName = ""

        # - this is ugly, but there's no static available 
        #   once we build a class for RTB, move this there
        self.oldPos = -1
        self.ShowPos()

        # --- finally - show it!
        self.Show(True)

    def BuildMenuBar(self):

        self.mainmenu = wx.MenuBar() 
# file menu
        fileMenu = wx.Menu()

        fileNew = fileMenu.Append(-1, "&New\tCtrl+N", "Create a new file")
        #wx.EVT_MENU(self, ID_NEW, self.OnFileNew) ## same as following
        self.Bind(wx.EVT_MENU,  self.OnFileNew, fileNew)

        # check if the application opens with an argument
        fileOpen = fileMenu.Append(-1, "&Open\tCtrl+O", "Open an existing file")
        self.Bind(wx.EVT_MENU,  self.OnFileOpen, fileOpen)
            
        fileSave = fileMenu.Append(-1, "&Save\tCtrl+S", "Save the active file")
        self.Bind(wx.EVT_MENU,  self.OnFileSave, fileSave)

        fileSaveAs =fileMenu.Append(-1, "&Save As...", "Save the active file with a new name")
        self.Bind(wx.EVT_MENU,  self.OnFileSaveAs, fileSaveAs)
        
        filePrint =fileMenu.Append(-1, "&Print\tCtrl+P", "Print the active file")        
        self.Bind(wx.EVT_MENU,  self.OnFilePrint, filePrint)

        """
        pnl = wx.Panel(self)
        self.pnl = pnl        
        # Set up a log window
        self.log = wx.TextCtrl(pnl, -1,
                              style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        """

        fileExit = fileMenu.Append(-1, "E&xit\tAlt+Q", "Exit the program")
        self.Bind(wx.EVT_MENU,  self.OnFileExit, fileExit)

# edit menu
        editMenu = wx.Menu()
        """
        # so ben ik Find icoontje kwijt!
        findItem = editMenu.Append(-1, '&Find\tCtrl-F', 'Find in opened text')
        findItem.SetBitmap(images.catalog['find'].GetBitmap())

        if 'wxMac' not in wx.PlatformInfo:
            findNextItem = editMenu.Append(-1, 'Find &Next\tF3', 'Find Next')
        else:
            findNextItem = editMenu.Append(-1, 'Find &Next\tCtrl-G', 'Find Next')
        findNextItem.SetBitmap(images.catalog['findnext'].GetBitmap())
        """
        findItem = wx.MenuItem(editMenu, -1, '&Find\tCtrl+F', 'Find in the opened text')
        findItem.SetBitmap(images.catalog['find'].GetBitmap())
        if 'wxMac' not in wx.PlatformInfo:
            findNextItem = wx.MenuItem(editMenu, -1, 'Find &Next\tF3', 'Find Next')
        else:
            findNextItem = wx.MenuItem(editMenu, -1, 'Find &Next\tCtrl+G', 'Find Next')
        findNextItem.SetBitmap(images.catalog['findnext'].GetBitmap())
	# GetBitmap = wx.lib.editor.images.GetBitmap  # in wxPython\lib\editor\images.py
        editMenu.AppendItem(findItem)
        editMenu.AppendItem(findNextItem)
        editMenu.AppendSeparator()
#
        self.Bind(wx.EVT_MENU, self.OnHelpFind,  findItem)
        self.Bind(wx.EVT_MENU, self.OnFindNext,  findNextItem)
        self.Bind(wx.EVT_FIND, self.OnFind)
        self.Bind(wx.EVT_FIND_NEXT, self.OnFind)
        self.Bind(wx.EVT_FIND_CLOSE, self.OnFindClose)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateFindItems, findItem)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateFindItems, findNextItem)
# Tool menu
        toolMenu = wx.Menu()
        easyMemo =toolMenu.Append(-1, "&Easy Memo\tCtrl+M", "Easy Memo")        
        self.Bind(wx.EVT_MENU,  self.OnEasyMemo, easyMemo)
        easyMemoP =toolMenu.Append(-1, "&Open Easy Memo\tCtrl+E", "Open Easy Memo")        
        self.Bind(wx.EVT_MENU,  self.OnEasyMemoOpen, easyMemoP)
        
# Help bar        
        helpMenu = wx.Menu()
#        helpMenu.Append(ID_ABOUT, "&About SmallEditor", "Display information about the program")
#        wx.EVT_MENU(self, ID_ABOUT, self.OnHelpAbout)
# the following does the same!
        helpItem = helpMenu.Append(-1, '&About SmallEditor', 'wxPython RULES!!!')
        self.Bind(wx.EVT_MENU, self.OnHelpAbout, helpItem)

# --- now add them to a menubar & attach it to the frame
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(editMenu, "&Edit")
        menuBar.Append(toolMenu, "&Tool")
        menuBar.Append(helpMenu, "&Help")
        self.SetMenuBar(menuBar)

#---------------------------------------
    def __del__(self):
        """ Class delete event: don't leave timer hanging around! """
        self.timer.stop()
        del self.timer

#---------------------------------------
    def Notify(self):
        """ Timer event """
        t = time.localtime(time.time())
        st = time.strftime(" %b-%d-%Y  %I:%M %p", t)
        # --- could also use self.sb.SetStatusText
        self.SetStatusText(st, SB_DATETIME)
#--------------------------------------
    def OnFilePrint(self, e):
        """ File|FilePrint event """
        docTitle = os.path.join(self.dirName, self.fileName)
        self.printer.Print(self.rtb.GetValue(), docTitle)

#--------------------------------------
    def OnEasyMemo(self, e):
        """ Tool/EasyMemo event """
       # os.system("Diary.exe &")
        subprocess.Popen(["Diary.exe"])

#--------------------------------------
    def OnEasyMemoOpen(self, e):
        """ Tool/EasyMemo event Open """
        
        self.OnFileOpenDirect( e, "diary.txt")

#---------------------------------------
    def OnFileExit(self, e):
        """ File|Exit event """
        if (self.rtb.IsModified() ):
            dlg = wx.MessageDialog(self, 
            "would like to save the file?",
            "Save file confirmation", 
            wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION)
            
            result = dlg.ShowModal()
            if( result == wx.ID_YES):                
 ### - Use the OnFileSave to save the file
                if self.OnFileSave(e):
                    self.SetTitle(APP_NAME + " - [" + self.fileName + "]")
                dlg.Destroy()
                self.Close(True)
                
            elif (result== wx.ID_NO): # NO                
                dlg.Destroy()                
                self.Close(True)
                
            elif (result == wx.ID_CANCEL): # Cancel
                dlg.Destroy()
            else:
                print "Never should be here!!!"
                                
        else: # nothing changed
            self.Close(True)

#---------------------------------------
    def OnFileNew(self, e):
        """ File|New event - Clear rtb. """
        self.fileName = ""
        self.dirName = ""
        self.rtb.SetValue("")
        self.PushStatusText("Starting new file", SB_INFO)
        self.ShowPos()

#---------------------------------------
    def OnFileOpen(self, e):
        """ File|Open event - Open dialog box. """
        dlg = wx.FileDialog(self, "Open", self.dirName, self.fileName,
                           "Text Files (*.txt)|*.txt|All Files|*.*", wx.OPEN)
        if (dlg.ShowModal() == wx.ID_OK):
            self.fileName = dlg.GetFilename()
            self.dirName = dlg.GetDirectory()

            ## - this will read in Unicode files (since I'm using Unicode wx.Python)
            ## - if NO-BREAK spaces (hex A0) in the text encounterd, it will only show blank!
            ## how to solve???
            if self.rtb.LoadFile(os.path.join(self.dirName, self.fileName)):
            #    print "self.rtb", self.rtb
                self.SetStatusText("Opened file: " + str(self.rtb.GetLastPosition()) + 
                                   " characters.", SB_INFO)
                self.ShowPos()
            else:
                self.SetStatusText("Error in opening file.", SB_INFO)

            ### - but we want just plain ASCII files, so:
            """
            try:
                f = file(os.path.join(self.dirName, self.fileName), 'r')
                self.rtb.SetValue(f.read())
                self.SetTitle(APP_NAME + " - [" + self.fileName + "]")
                self.SetStatusText("Opened file: " + str(self.rtb.GetLastPosition()) +
                                   " characters.", SB_INFO)
                self.ShowPos()
                f.close()
            except:
                self.PushStatusText("Error in opening file.", SB_INFO)
            """
        dlg.Destroy()

#---------------------------------------
    def OnFileOpenDirect(self, e, fileName = None):
        """ File|Open event Direct from arg. is not Unicode compatible """
        if fileName == None:
            #self.fileName = sys.argv[1].decode('utf-8') #not yet working for chinese
            #self.fileName = sys.argv[1].decode(sys.getfilesystemencoding()) #not yet working for chinese
            self.fileName = sys.argv[1]
        else:
            self.fileName = fileName

        if self.rtb.LoadFile(self.fileName):
            self.SetStatusText("Opened file: " + str(self.rtb.GetLastPosition()) + 
                               " characters.", SB_INFO)
            self.ShowPos()
        else:
            self.SetStatusText("Error in opening file.", SB_INFO)
        
        self.rtb.SetFocus() # necessary!!!
      #  e.Skip()
#---------------------------------------
    def OnFileSave(self, e):
        """ File|Save event - Just Save it if it's got a name. """
        if(len(sys.argv)) == 2: #for direct open file
            self.fileName = sys.argv[1]

        #if (self.fileName != "") and (self.dirName != ""): # dirName is not necessary to check (for direct open is not easy)
        if (self.fileName != ""):
            # try to save with Unicode text in the file
            if self.rtb.SaveFile(os.path.join(self.dirName, self.fileName)):
                self.SetStatusText("Saved file: " + str(self.rtb.GetLastPosition()) + 
                                   " characters.", SB_INFO)
            else:
                self.SetStatusText("Error in saving file (Unicode).", SB_INFO)

            """
            try: # only valid for Ascii
               # The following does not work for Unicode 
               # f = file(os.path.join(self.dirName, self.fileName), 'w','utf-8')
                f = file(os.path.join(self.dirName, self.fileName), 'w')
                f.write(self.rtb.GetValue())
                self.PushStatusText("Saved file: " + str(self.rtb.GetLastPosition()) +
                                    " characters.", SB_INFO)
                f.close()
                return True
            except:
                self.PushStatusText("Error in saving file: file will be empty! Please remove the
                    last changes and save it again!", SB_INFO)
                # file is empty due to the error!
                return False
            """
        else:
            ### - If no name yet, then use the OnFileSaveAs to get name/directory
            return self.OnFileSaveAs(e)

#--------------------------------------
    def OnFileSaveAs(self, e):
        """ File|SaveAs event - Prompt for File Name. """
        ret = False
        dlg = wx.FileDialog(self, "Save As", self.dirName, self.fileName,
                           "Text Files (*.txt)|*.txt|All Files|*.*", wx.SAVE)
        if (dlg.ShowModal() == wx.ID_OK):
            self.fileName = dlg.GetFilename()
            self.dirName = dlg.GetDirectory()
            ## should check if the file exists
            if os.path.exists(os.path.join(self.dirName, self.fileName)):
                dlg = wx.MessageDialog(self,"File already exists! Do you want to replace it?",
                "Save as file confirmation", wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION)
            
                result = dlg.ShowModal()
                if( result == wx.ID_YES):                

                    ### - Use the OnFileSave to save the file
                    if self.OnFileSave(e):
                        self.SetTitle(APP_NAME + " - [" + self.fileName + "]")
                        ret = True
            else: # file not exists
                ### - Use the OnFileSave to save the file
                if self.OnFileSave(e):
                    self.SetTitle(APP_NAME + " - [" + self.fileName + "]")
                    ret = True

        dlg.Destroy()

        return ret

#--------------------------------------
    def OnHelpFind(self, event):
        if self.finddlg != None:
            return
        
        self.finddlg = wx.FindReplaceDialog(self, self.finddata, "Find",
                        wx.FR_NOMATCHCASE | wx.FR_NOWHOLEWORD)
        self.finddlg.Show(True)

    def OnUpdateFindItems(self, evt):
        evt.Enable(self.finddlg == None)

   #---------------------------------------------
    def OnFind(self, event):
        # these are original
        #  editor = self.codePage.editor
        #  end = editor.GetLastPosition()
        end= self.rtb.GetLastPosition()
        textstring = self.rtb.GetRange(0, end).lower()
        findstring = self.finddata.GetFindString().lower()
        backward = not (self.finddata.GetFlags() & wx.FR_DOWN)
        if backward:
            start = self.rtb.GetSelection()[0]
            loc = textstring.rfind(findstring, 0, start)
        else:
            start = self.rtb.GetSelection()[1]
            loc = textstring.find(findstring, start)
        if loc == -1 and start != 0:
            # string not found, start at beginning
            if backward:
                start = end
                loc = textstring.rfind(findstring, 0, start)
            else:
                start = 0
                loc = textstring.find(findstring, start)
        if loc == -1:
            dlg = wx.MessageDialog(self, 'Find String Not Found',
                          'Find String Not Found in Demo File',
                          wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        if self.finddlg:
            if loc == -1:
                self.finddlg.SetFocus()
                return
            else:
                self.finddlg.Destroy()
                self.finddlg = None

        self.rtb.SetFocus() # Needed for OpenFileDirect!

        self.rtb.ShowPosition(loc)
        self.rtb.SetSelection(loc, loc + len(findstring))

    def OnFindNext(self, event):
        if self.finddata.GetFindString():
            self.OnFind(event)
        else:
            self.OnHelpFind(event)

    def OnFindClose(self, event):
        event.GetDialog().Destroy()
        self.finddlg = None

#---------------------------------------
    def OnShowFind(self, e):
        """ Find|Something event """
        data = wx.FindReplaceData()
        data.SetFlags(wx.FR_DOWN) # search down by default
#	    
#        #data.SetReplaceString(self._replaceString)
        dlg = wx.FindReplaceDialog(self, data, "Find")
        dlg.data = data  # save a reference to it...
        dlg.Show(True)
#---------------------------------------
    def OnHelpAbout(self, e):
        """ Help|About event """
        title = self.GetTitle()
        title1 = title + "\nBugs found? Please contact: ming_ruan@yahoo.com"
        d = wx.MessageDialog(self, "About " + title1, title, wx.ICON_INFORMATION | wx.OK)
        d.ShowModal()
        d.Destroy()

#---------------------------------------
    def OnRtbKeyUp(self, e):
        """ Update Row/Col indicator based on position """
        self.ShowPos()
        e.Skip()

#---------------------------------------
    def ShowPos(self):
        """ Update Row/Col indicator """
        (bPos,ePos) = self.rtb.GetSelection()
        if (self.oldPos != ePos):
            (c,r) = self.rtb.PositionToXY(ePos)
            self.SetStatusText(" " + str((r+1,c+1)), SB_ROWCOL)
        self.oldPos = ePos

#---------------------------------------
    def AddLine(self, sizer):
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND)

    def AddText(self, sizer, text1, text2='', lang='', font=None):
        # create some controls
        lang  = wx.StaticText(self, -1, lang)
        text1 = wx.StaticText(self, -1, text1)
        text2 = wx.StaticText(self, -1, text2, style=wx.ALIGN_RIGHT)
        if font is not None:
            text1.SetFont(font)

        # put them in a sizer
        row = wx.BoxSizer(wx.HORIZONTAL)
        row.Add(lang)
        row.Add((15,10))
        row.Add(text1, 1, wx.EXPAND)
        row.Add(text2)

        # put the row in the main sizer
        sizer.Add(row, 0, wx.EXPAND|wx.ALL, 5)

#-------------------------------------------------------------------------------
def onDummy(evt):

#    if evt.GetActive():
#        print "Activate"
#    else:
#        print "Deactivate"
        
    return

# --- Program Entry Point
#app = wx.PySimpleApp()

app = wx.App(False)

# --- note: Title never gets used!
frame = smallAppFrame(None, -1, "Small wxPython Application")

if(len(sys.argv)) == 2:
    frame.Bind(wx.EVT_ACTIVATE, onDummy)  # dummy!

# frame.Show(True)  # - now shown in class __init__
#app = MyApp(False)
app.MainLoop()
# only be here when app terminates 
#pycallgraph.make_dot_graph('test.png')
"""
+-------------------+
|      wx.Frame     |
+-------------------+
         .                                            
        /_\                                           
         |                                            
         |                                            
         |                                            
         |                                            
         |                                            
+-------------------+                                 
|   smallAppFrame   |                                 
|-------------------|                                 
| overviewText      |          
| printer           |  ---->  [ Printer ]  
| codePage          |          
| finddlg           |  ---->  [ wx.FindReplaceDialog ]
| finddata          |  ---->  [ wx.FindReplaceData]         
| timer             |  ---->  [ wx.PyTimer ]          
| rtb               |  ---->  [ wx.TextCtrl ]             
| sizer             |  ---->  [ wx.BoxSizer ]                                 
| dirName           |                                 
| fileName          |                                 
| oldPos            |                                 
| mainmenu          |  ---->  [ wx.MenuBar ]                         
|-------------------|                                 
| __init__          |                                 
| BuildMenuBar      |                                 
| __del__           |                                 
| Notify            |                                 
| OnFilePrint       |                                 
| OnEasyMemo        |                                 
| OnEasyMemoOpen    |                                 
| OnFileExit        |                                 
| OnFileNew         |                                 
| OnFileOpen        |                                 
| OnFileOpenDirect  |                                 
| OnFileSave        |                                 
| OnFileSaveAs      |                                 
| OnHelpFind        |                                 
| OnUpdateFindItems |                                 
| OnFind            |                                 
| OnFindNext        |                                 
| OnFindClose       |                                 
| OnShowFind        |                                 
| OnHelpAbout       |                                 
| OnRtbKeyUp        |                                 
| ShowPos           |                                 
| AddLine           |                                 
| AddText           |                                 
+-------------------+                                 
                                                             
                                                             
+---------+       +--------------------+       +------------+
| Printer |       | wx.FindReplaceData |       | wx.PyTimer |
+---------+       +--------------------+       +------------+
                                                          
                                                          
+-------------+       +-------------+       +------------+
| wx.TextCtrl |       | wx.BoxSizer |       | wx.MenuBar |
+-------------+       +-------------+       +------------+
                        
                        
+----------------------+
| wx.FindReplaceDialog |
+----------------------+

"""
