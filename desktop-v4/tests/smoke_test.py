import os, sys
from pathlib import Path
os.environ.setdefault("QT_QPA_PLATFORM","offscreen")
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from PySide6.QtWidgets import QApplication
from main import Main, tool

app=QApplication([])
window=Main()
assert window.layout.count() if hasattr(window.layout,"count") else True
assert window.windowTitle().startswith("MF VIDEO STUDIO AI")
assert window.res.count() == 2
assert window.fps.count() == 5
assert tool("ffmpeg") and tool("ffprobe"), "Bundled FFmpeg/FFprobe missing"
print("Desktop smoke test PASS")
