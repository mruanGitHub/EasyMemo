;NSIS Script For SmallEditor

;Background Colors
;BGGradient 0000FF 000000 FFFFFF
;Title Of Your Application

;Do A CRC Check
;CRCCheck On
;
; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "SmallEditor"
!define PRODUCT_VERSION "1.1"
!define PRODUCT_PUBLISHER "Ab Ovo Int."
!define PRODUCT_WEB_SITE "http://www.ab-ovo.com"
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
OutFile "SmallEditorSetup.exe"

;The Default Installation Directory
InstallDir "C:\SmallEditor"

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
!define MUI_FINISHPAGE_RUN "$INSTDIR\SmallEditor.exe"
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
  File "C:\Python27\own python files\SmallApp\dist\Diary.exe"
  File "C:\Python27\own python files\SmallApp\dist\SmallEditor.exe"
  File "C:\Python27\own python files\SmallApp\dist\w9xpopen.exe"
  File "C:\Python27\own python files\SmallApp\dist\_hashlib.pyd"
  File "C:\Python27\own python files\SmallApp\dist\bz2.pyd"
  File "C:\Python27\own python files\SmallApp\dist\select.pyd"
  File "C:\Python27\own python files\SmallApp\dist\unicodedata.pyd"
  File "C:\Python27\own python files\SmallApp\dist\wx._controls_.pyd"
  File "C:\Python27\own python files\SmallApp\dist\wx._core_.pyd"
  File "C:\Python27\own python files\SmallApp\dist\wx._gdi_.pyd"
  File "C:\Python27\own python files\SmallApp\dist\wx._misc_.pyd"
  File "C:\Python27\own python files\SmallApp\dist\wx._windows_.pyd"
  File "C:\Python27\own python files\SmallApp\dist\msvcp90.dll"
  File "C:\Python27\own python files\SmallApp\dist\python27.dll"
  File "C:\Python27\own python files\SmallApp\dist\wxbase30u_net_vc90.dll"
  File "C:\Python27\own python files\SmallApp\dist\wxbase30u_vc90.dll"
  File "C:\Python27\own python files\SmallApp\dist\wxmsw30u_adv_vc90.dll"
  File "C:\Python27\own python files\SmallApp\dist\wxmsw30u_core_vc90.dll"
  File "C:\Python27\own python files\SmallApp\dist\wxmsw30u_html_vc90.dll"
  File "C:\Python27\own python files\SmallApp\dist\SmallEditor.ico"
  File "C:\Python27\own python files\SmallApp\dist\library.zip"
  File "C:\Python27\own python files\SmallApp\readme.txt"
  File "C:\Python27\own python files\SmallApp\diary.txt"

  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SmallEditor" "DisplayName" "SmallEditor"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\SmallEditor" "UninstallString" "$INSTDIR\Uninst.exe"
WriteUninstaller "Uninst.exe"
SectionEnd

Section "Shortcuts"
  ;Add Shortcuts
  CreateDirectory "$SMPROGRAMS\SmallEditor"
  CreateShortCut "$SMPROGRAMS\SmallEditor\SmallEditor.lnk" "$INSTDIR\SmallEditor.exe" "" "$INSTDIR\SmallEditor.exe" 0
  CreateShortCut "$DESKTOP\SmallEditor.lnk" "$INSTDIR\SmallEditor.exe"
SectionEnd

UninstallText "This will uninstall SmallEditor from your system"

Section Uninstall
  ;Delete Files
  Delete "$INSTDIR\SmallEditor.exe"
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
  Delete "$INSTDIR\wxbase30u_vc90.dll"
  Delete "$INSTDIR\wxbase30u_net_vc90.dll"
  Delete "$INSTDIR\wxmsw30u_core_vc90.dll"
  Delete "$INSTDIR\wxmsw30u_adv_vc90.dll"
  Delete "$INSTDIR\wxmsw30u_html_vc90.dll"
  Delete "$INSTDIR\SmallEditor.ico"
  Delete "$INSTDIR\library.zip"
  Delete "$INSTDIR\readme.txt"
  Delete "$INSTDIR\diary.txt"
  Delete "$DESKTOP\SmallEditor.lnk"

  ;Delete Start Menu Shortcuts
  Delete "$SMPROGRAMS\SmallEditor\*.*"
  RmDir "$SMPROGRAMS\SmallEditor"

  ;Delete Uninstaller And Unistall Registry Entries
  Delete "$INSTDIR\Uninst.exe"
  DeleteRegKey HKEY_LOCAL_MACHINE "SOFTWARE\SmallEditor"
  DeleteRegKey HKEY_LOCAL_MACHINE "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\SmallEditor"
  RMDir "$INSTDIR"
SectionEnd

