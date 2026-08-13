#define MyAppName "QuickBill Pro"
#define MyAppVersion "3.0.0"
#define MyAppPublisher "Kartik Bansode"
#define MyAppExeName "QuickBill.exe"

[Setup]

; ============================================================
; Application Identity
; ============================================================

AppId={{E8F66E52-8F77-4C6F-90A6-61E4B6F57A01}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}

AppPublisher={#MyAppPublisher}
AppPublisherURL=https://github.com/kartikbansode/quickbill
AppSupportURL=https://github.com/kartikbansode/quickbill/issues
AppUpdatesURL=https://github.com/kartikbansode/quickbill/releases

; ============================================================
; Installation
; ============================================================

DefaultDirName={autopf}\QuickBill
DefaultGroupName={#MyAppName}

PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

DisableProgramGroupPage=yes
DisableDirPage=no

; ============================================================
; Output
; ============================================================

OutputDir=..\release
OutputBaseFilename=QuickBill_Setup_v{#MyAppVersion}

; ============================================================
; Branding
; ============================================================

SetupIconFile=..\assets\images\logo.ico

WizardStyle=modern
WizardImageFile=wizard.bmp
WizardSmallImageFile=wizard_small.bmp

LicenseFile=..\licenses\LICENSE.txt

; ============================================================
; Compression
; ============================================================

Compression=lzma2/max
SolidCompression=yes
CompressionThreads=auto
LZMAUseSeparateProcess=yes

; ============================================================
; Windows Architecture
; ============================================================

ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; ============================================================
; Uninstaller
; ============================================================

Uninstallable=yes
UninstallDisplayName={#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}

; ============================================================
; Windows File Version Information
; ============================================================

VersionInfoVersion=3.0.0.0
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription=Professional Desktop Billing and POS Management System
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}
VersionInfoCopyright=Copyright © 2026 Kartik Bansode. All Rights Reserved.

; ============================================================
; Installer Behavior
; ============================================================

SetupLogging=yes
CloseApplications=yes
RestartApplications=no

AllowNoIcons=yes
ShowLanguageDialog=no


[Languages]

Name: "english"; MessagesFile: "compiler:Default.isl"


[Tasks]

Name: "desktopicon"; \
    Description: "Create a desktop shortcut"; \
    GroupDescription: "Additional shortcuts:"; \
    Flags: unchecked


[Files]

Source: "..\dist\QuickBill.exe"; \
    DestDir: "{app}"; \
    Flags: ignoreversion


[Icons]

Name: "{group}\{#MyAppName}"; \
    Filename: "{app}\{#MyAppExeName}"

Name: "{autodesktop}\{#MyAppName}"; \
    Filename: "{app}\{#MyAppExeName}"; \
    Tasks: desktopicon


[Run]

Filename: "{app}\{#MyAppExeName}"; \
    Description: "Launch {#MyAppName}"; \
    Flags: nowait postinstall skipifsilent