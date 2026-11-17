#define AppName "MF VIDEO STUDIO AI PROFESSIONAL"
#define AppVersion "4.0.0"
#define AppExe "MF VIDEO STUDIO AI.exe"
[Setup]
AppId={{9E50A48D-7A31-4E6F-9C18-6A23D2C4A440}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher=MADE ADJA
DefaultDirName={autopf}\MF VIDEO STUDIO AI
DefaultGroupName={#AppName}
OutputDir=..\release
OutputBaseFilename=MF_VIDEO_STUDIO_AI_SETUP_V4
ArchitecturesInstallIn64BitMode=x64
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
[Files]
Source: "..\dist\MF VIDEO STUDIO AI\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion
[Icons]
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\{#AppExe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExe}"; Tasks: desktopicon
[Tasks]
Name: "desktopicon"; Description: "Create desktop shortcut"; GroupDescription: "Additional icons:"
[Run]
Filename: "{app}\{#AppExe}"; Description: "Launch MF VIDEO STUDIO AI"; Flags: postinstall nowait skipifsilent
