#define AppName "TaskAutomationApp"
#ifndef AppVersion
  #define AppVersion "v0.0.0"
#endif
#define Publisher "Internal Team"
#define SourcePath "..\\dist\\TaskAutomationApp\\"
#define OutputPath "..\\release\\"

[Setup]
AppId={{9D2CB1A8-BC13-4707-BA04-C0FBB2C64039}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#Publisher}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
OutputDir={#OutputPath}
OutputBaseFilename={#AppName}-{#AppVersion}-setup
Compression=lzma
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
WizardStyle=modern
SetupLogging=yes

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na área de trabalho"; GroupDescription: "Atalhos:"

[Files]
Source: "{#SourcePath}*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\TaskAutomationApp.exe"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\TaskAutomationApp.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\TaskAutomationApp.exe"; Description: "Executar {#AppName}"; Flags: nowait postinstall skipifsilent
