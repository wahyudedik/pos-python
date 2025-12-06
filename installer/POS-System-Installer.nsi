; NSIS Installer Script untuk POS Offline System
; Requires NSIS 3.0 atau lebih tinggi
; Download dari: https://nsis.sourceforge.io

!include "MUI2.nsh"
!include "x64.nsh"

; Name dan file
Name "POS Offline System"
OutFile "dist\POS-System-Installer-v1.0.0.exe"

; Default installation folder
InstallDir "$PROGRAMFILES\POS-System"

; Get installation folder from registry if available
InstallDirRegKey HKCU "Software\POS-System" ""

; Request application privileges for Windows Vista and higher
RequestExecutionLevel admin

;================================
; Variables
;
Var StartMenuFolder

;================================
; MUI Settings
;
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Header\modern.bmp"
!define MUI_WELCOMEFINISHPAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Wizard\modern.bmp"

;================================
; Pages
;
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

;================================
; Language
;
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "Indonesian"

;LangString welcome ${LANG_ENGLISH} "Selamat datang di POS Offline System"
;LangString welcome ${LANG_INDONESIAN} "Selamat datang di POS Offline System"

;================================
; Installer sections
;

Section "POS System Application" SecApp
  SetOutPath "$INSTDIR"
  
  ; Copy application files
  File /r "dist\POS-System\*.*"
  
  ; Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
  ; Write registry keys
  WriteRegStr HKCU "Software\POS-System" "" "$INSTDIR"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\POS-System" \
    "DisplayName" "POS Offline System"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\POS-System" \
    "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\POS-System" \
    "DisplayVersion" "1.0.0"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\POS-System" \
    "Publisher" "Wahyu Dedik"
  
  ; Create start menu entries
  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
    CreateShortCut "$SMPROGRAMS\$StartMenuFolder\POS System.lnk" "$INSTDIR\POS-System.exe"
    CreateShortCut "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
  !insertmacro MUI_STARTMENU_WRITE_END
  
  ; Create desktop shortcut
  CreateShortCut "$DESKTOP\POS System.lnk" "$INSTDIR\POS-System.exe"
  
SectionEnd

Section "Create Database" SecDB
  SetOutPath "$INSTDIR\data"
  
  ; Database akan dibuat otomatis saat aplikasi pertama kali dijalankan
  ; Tidak perlu copy database template
  
SectionEnd

Section "Start Menu & Desktop Shortcuts" SecShortcuts
  ; Shortcuts already created in SecApp
SectionEnd

;================================
; Descriptions
;
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecApp} "POS Offline System Application"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecDB} "Create application database"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecShortcuts} "Create shortcuts for easy access"
!insertmacro MUI_FUNCTION_DESCRIPTION_END

;================================
; Uninstaller sections
;
Section "Uninstall"
  ; Remove application files
  RMDir /r "$INSTDIR"
  
  ; Remove start menu entries
  !insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuFolder
  RMDir /r "$SMPROGRAMS\$StartMenuFolder"
  
  ; Remove desktop shortcut
  Delete "$DESKTOP\POS System.lnk"
  
  ; Remove registry keys
  DeleteRegKey HKCU "Software\POS-System"
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\POS-System"
  
SectionEnd
