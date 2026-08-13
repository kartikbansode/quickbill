#define MyAppName "QuickBill"
#define MyAppVersion "3.0.0"
#define MyAppPublisher "Essenc Technologies"
#define MyAppExeName "QuickBill.exe"

[Setup]
AppId={{E8F66E52-8F77-4C6F-90A6-61E4B6F57A01}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}

AppPublisher={#MyAppPublisher}
AppPublisherURL=
AppSupportURL=
AppUpdatesURL=

DefaultDirName={autopf}\QuickBill
DefaultGroupName=QuickBill

OutputDir=..\release
OutputBaseFilename=QuickBill_Setup_v3.0.0

SetupIconFile=..\assets\images\logo.ico

WizardImageFile=wizard.bmp
WizardSmallImageFile=wizard_small.bmp

LicenseFile=..\licenses\LICENSE.txt

WizardStyle=modern

Compression=lzma2/max
SolidCompression=yes
CompressionThreads=auto
LZMAUseSeparateProcess=yes

ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

DisableProgramGroupPage=yes
DisableDirPage=no

UninstallDisplayIcon={app}\QuickBill.exe

VersionInfoVersion=3.0.0.0
VersionInfoCompany=Essenc Technologies
VersionInfoDescription=Professional Barcode Billing Software
VersionInfoProductName=QuickBill
VersionInfoProductVersion=3.0.0
VersionInfoCopyright=Copyright © 2026 Essenc Technologies. All Rights Reserved.

SetupLogging=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: desktopicon; Description: "Create a Desktop Shortcut"; GroupDescription: "Additional Tasks:"; Flags: unchecked

[Files]
Source: "..\dist\QuickBill.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\QuickBill"; Filename: "{app}\QuickBill.exe"
Name: "{autodesktop}\QuickBill"; Filename: "{app}\QuickBill.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\QuickBill.exe"; Description: "Launch QuickBill"; Flags: nowait postinstall skipifsilent