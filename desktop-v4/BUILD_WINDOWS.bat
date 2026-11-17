@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul || (echo Python 3.11 required on build runner.& exit /b 1)
if not exist vendor mkdir vendor
if not exist vendor\ffmpeg.zip powershell -NoProfile -Command "Invoke-WebRequest 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip' -OutFile 'vendor\ffmpeg.zip'"
if errorlevel 1 exit /b 1
if not exist vendor\ffmpeg-extract mkdir vendor\ffmpeg-extract
tar -xf vendor\ffmpeg.zip -C vendor\ffmpeg-extract
for /d %%D in (vendor\ffmpeg-extract\ffmpeg-*) do (
  if exist "%%D\bin\ffmpeg.exe" (
    if not exist bin mkdir bin
    copy /y "%%D\bin\ffmpeg.exe" bin\ffmpeg.exe >nul
    copy /y "%%D\bin\ffprobe.exe" bin\ffprobe.exe >nul
  )
)
if not exist bin\ffmpeg.exe (echo FFmpeg extraction failed.& exit /b 1)
py -3 -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 exit /b 1
python -c "from PySide6.QtWidgets import QApplication; from PySide6.QtMultimedia import QMediaPlayer; print('Qt import smoke test OK')"
pyinstaller --noconfirm --clean --windowed --name "MF VIDEO STUDIO AI" --add-data "bin;bin" src\main.py
if errorlevel 1 exit /b 1
echo Build folder ready: dist\MF VIDEO STUDIO AI
