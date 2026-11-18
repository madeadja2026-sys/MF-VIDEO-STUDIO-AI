$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$Python = (Get-Command python).Source
if (!(Test-Path "bin\ffmpeg.exe") -or !(Test-Path "bin\ffprobe.exe")) {
    New-Item -ItemType Directory -Force -Path "vendor" | Out-Null
    Invoke-WebRequest "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip" -OutFile "vendor\ffmpeg.zip"
    Expand-Archive -Force "vendor\ffmpeg.zip" "vendor\ffmpeg-expanded"
    $ffmpeg = Get-ChildItem "vendor\ffmpeg-expanded" -Filter ffmpeg.exe -Recurse | Select-Object -First 1
    $ffprobe = Get-ChildItem "vendor\ffmpeg-expanded" -Filter ffprobe.exe -Recurse | Select-Object -First 1
    if (!$ffmpeg -or !$ffprobe) { throw "FFmpeg/FFprobe binaries not found after extraction." }
    New-Item -ItemType Directory -Force -Path "bin" | Out-Null
    Copy-Item $ffmpeg.FullName "bin\ffmpeg.exe" -Force
    Copy-Item $ffprobe.FullName "bin\ffprobe.exe" -Force
}
& $Python -m venv .venv
$VenvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
& $VenvPython -m pip install --upgrade pip
& $VenvPython -m pip install -r requirements.txt
& $VenvPython -c "from PySide6.QtWidgets import QApplication; from PySide6.QtMultimedia import QMediaPlayer; print('Qt import check passed')"
& $VenvPython -m py_compile src\app.py
& $VenvPython -m PyInstaller --noconfirm --clean --windowed --name "MF VIDEO STUDIO AI" --add-data "bin;bin" --collect-all PySide6 src\app.py
if ($LASTEXITCODE -ne 0) { throw "PyInstaller build failed." }
if (!(Test-Path "dist\MF VIDEO STUDIO AI\MF VIDEO STUDIO AI.exe")) { throw "Expected application EXE was not produced." }
Write-Host "Application package created successfully."
