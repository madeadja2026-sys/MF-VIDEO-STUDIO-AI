#define AppName "MF VIDEO STUDIO AI PROFESSIONAL"
#define AppVersion "4.0.0"
#define AppExe "MF VIDEO STUDIO AI.exe"
[Setup]
AppId={{D47C6B28-2D56-4B1D-8B6A-4B7E3D44A401}
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
Filename: "{app}\{#AppExe}"; Description: "Launch application"; Flags: postinstall nowait skipifsilent
