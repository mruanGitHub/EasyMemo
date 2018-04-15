;NSIS Script For easyMemo

;Background Colors
;BGGradient 0000FF 000000 FFFFFF
;Title Of Your Application

;Do A CRC Check
;CRCCheck On
;
; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "easyMemo"
!define PRODUCT_VERSION "1.2"
!define PRODUCT_PUBLISHER "Priva b.v."
!define PRODUCT_WEB_SITE "http://www.priva.nl"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths${PRODUCT_NAME}"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"
!define PRODUCT_STARTMENU_REGVAL "NSIS:StartMenuDir"

;MUI 1.67 compatible ------
!include "MUI.nsh"
; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"
;Output File Name
OutFile "easyMemoSetup.exe"

;The Default Installation Directory
InstallDir "C:\easyMemo"

;The text to prompt the user to enter a directory
DirText "Please select the folder below"
; Welcome page
!insertmacro MUI_PAGE_WELCOME
; License page
;;!insertmacro MUI_PAGE_LICENSE "licence.txt"
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
!define MUI_FINISHPAGE_RUN "$INSTDIR\easyMemo.exe"
!define MUI_FINISHPAGE_SHOWREADME "$INSTDIR\readme.txt"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "English"

; MUI end ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
;InstallDir "$PROGRAMFILES\Ab Ovo\TLSetup"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show

Section "Install"
  ;Install Files
  SetOutPath $INSTDIR
  SetCompress Auto
  SetOverwrite IfNewer
  File ".\dist\Diary.exe"
  File ".\dist\easyMemo.exe"
  File ".\dist\w9xpopen.exe"
  File ".\dist\_hashlib.pyd"
  File ".\dist\bz2.pyd"
  File ".\dist\select.pyd"
  File ".\dist\unicodedata.pyd"
  File ".\dist\wx._controls_.pyd"
  File ".\dist\wx._core_.pyd"
  File ".\dist\wx._gdi_.pyd"
  File ".\dist\wx._misc_.pyd"
  File ".\dist\wx._windows_.pyd"
  File ".\dist\msvcp90.dll"
  File ".\dist\python27.dll"
  File ".\dist\wxbase28uh_net_vc.dll"
  File ".\dist\wxbase28uh_vc.dll"
  File ".\dist\wxmsw28uh_adv_vc.dll"
  File ".\dist\wxmsw28uh_core_vc.dll"
  File ".\dist\wxmsw28uh_html_vc.dll"
  File ".\dist\easyMemo.ico"
  File ".\dist\library.zip"
  File ".\readme.txt"
  File ".\diary.txt"

  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\easyMemo" "DisplayName" "easyMemo"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\easyMemo" "UninstallString" "$INSTDIR\Uninst.exe"
WriteUninstaller "Uninst.exe"
SectionEnd

Section "Shortcuts"
  ;Add Shortcuts
  CreateDirectory "$SMPROGRAMS\easyMemo"
  CreateShortCut "$SMPROGRAMS\easyMemo\easyMemo.lnk" "$INSTDIR\easyMemo.exe" "" "$INSTDIR\easyMemo.exe" 0
  CreateShortCut "$DESKTOP\easyMemo.lnk" "$INSTDIR\easyMemo.exe"
SectionEnd

UninstallText "This will uninstall easyMemo from your system"

Section Uninstall
  ;Delete Files
  Delete "$INSTDIR\easyMemo.exe"
  Delete "$INSTDIR\Diary.exe"
  Delete "$INSTDIR\w9xpopen.exe"
  Delete "$INSTDIR\_hashlib.pyd"
  Delete "$INSTDIR\bz2.pyd"
  Delete "$INSTDIR\select.pyd"
  Delete "$INSTDIR\unicodedata.pyd"
  Delete "$INSTDIR\wx._controls_.pyd"
  Delete "$INSTDIR\wx._core_.pyd"
  Delete "$INSTDIR\wx._gdi_.pyd"
  Delete "$INSTDIR\wx._misc_.pyd"
  Delete "$INSTDIR\wx._windows_.pyd"
  Delete "$INSTDIR\msvcp90.dll"
  Delete "$INSTDIR\python27.dll"
  Delete "$INSTDIR\wxbase28uh_net_vc.dll"
  Delete "$INSTDIR\wxbase28uh_vc.dll"
  Delete "$INSTDIR\wxmsw28uh_adv_vc.dll"
  Delete "$INSTDIR\wxmsw28uh_core_vc.dll"
  Delete "$INSTDIR\wxmsw28uh_html_vc.dll"
  Delete "$INSTDIR\easyMemo.ico"
  Delete "$INSTDIR\library.zip"
  Delete "$INSTDIR\readme.txt"
  Delete "$INSTDIR\diary.txt"
  Delete "$DESKTOP\easyMemo.lnk"

  ;Delete Start Menu Shortcuts
  Delete "$SMPROGRAMS\easyMemo\*.*"
  RmDir "$SMPROGRAMS\easyMemo"

  ;Delete Uninstaller And Unistall Registry Entries
  Delete "$INSTDIR\Uninst.exe"
  DeleteRegKey HKEY_LOCAL_MACHINE "SOFTWARE\easyMemo"
  DeleteRegKey HKEY_LOCAL_MACHINE "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\easyMemo"
  RMDir "$INSTDIR"
SectionEnd
