import sys, os, shutil, subprocess, json
from pathlib import Path
from PySide6.QtCore import Qt, QUrl, QTimer
from PySide6.QtWidgets import *
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget

APP = "MF VIDEO STUDIO AI PROFESSIONAL V4.0"
ROOT = Path(sys.executable).resolve().parent if getattr(sys,"frozen",False) else Path(__file__).resolve().parents[1]
BUNDLE = Path(getattr(sys,"_MEIPASS",ROOT))
BIN = BUNDLE/"bin"
if not BIN.exists(): BIN = ROOT/"bin"
def tool(name):
    local=BIN/(name+".exe")
    return str(local) if local.exists() else shutil.which(name)

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP+" | MADE ADJA")
        self.resize(1450,900); self.setMinimumSize(1050,680)
        self.videos=[]; self.audios=[]; self.current=None
        self.player=QMediaPlayer(self); self.audioout=QAudioOutput(self)
        self.player.setAudioOutput(self.audioout)
        self.build(); self.theme(); self.check_tools()
    def build(self):
        c=QWidget(); self.setCentralWidget(c); root=QVBoxLayout(c)
        head=QHBoxLayout(); title=QLabel("MF VIDEO STUDIO AI"); title.setObjectName("brand")
        head.addWidget(title); brand=QLabel("PROFESSIONAL V4.0  •  MADE ADJA"); brand.setObjectName("cyan")
        head.addWidget(brand); head.addStretch(); self.engine=QLabel("ENGINE CHECK"); head.addWidget(self.engine); root.addLayout(head)
        bar=QHBoxLayout()
        for label,fn in [("＋ Import Video",self.add_video),("♫ Import Audio",self.add_audio),("Save Project",self.save),("Open Project",self.open_project),("Export MP4",self.export)]:
            b=QPushButton(label); b.clicked.connect(fn); bar.addWidget(b)
        bar.addStretch(); root.addLayout(bar)
        split=QSplitter(Qt.Horizontal); root.addWidget(split,1)
        left=QWidget(); ll=QVBoxLayout(left); ll.addWidget(self.heading("MEDIA BIN"))
        self.media=QListWidget(); self.media.currentRowChanged.connect(self.select_media); ll.addWidget(self.media,1)
        rm=QPushButton("Remove selected"); rm.clicked.connect(self.remove); ll.addWidget(rm); split.addWidget(left)
        center=QWidget(); cl=QVBoxLayout(center)
        row=QHBoxLayout(); row.addWidget(self.heading("PROGRAM MONITOR")); row.addStretch()
        row.addWidget(QLabel("Layout")); self.layout=QComboBox()
        self.layout.addItems(["Single Frame","2 Split Vertical","2 Split Horizontal","3 Split Columns","3 Split Main + Two","Asymmetric Split","Free Layout"])
        row.addWidget(self.layout); cl.addLayout(row)
        self.preview=QVideoWidget(); self.player.setVideoOutput(self.preview); cl.addWidget(self.preview,1)
        controls=QHBoxLayout(); play=QPushButton("▶ Play / Pause"); play.clicked.connect(self.toggle); controls.addWidget(play)
        self.seek=QSlider(Qt.Horizontal); self.seek.setRange(0,0); self.seek.sliderMoved.connect(self.player.setPosition)
        self.player.positionChanged.connect(self.seek.setValue); self.player.durationChanged.connect(lambda d:self.seek.setRange(0,d))
        controls.addWidget(self.seek,1); self.clock=QLabel("00:00"); controls.addWidget(self.clock)
        self.player.positionChanged.connect(lambda ms:self.clock.setText(f"{ms//60000:02d}:{(ms//1000)%60:02d}"))
        cl.addLayout(controls); split.addWidget(center)
        right=QWidget(); rl=QVBoxLayout(right); rl.addWidget(self.heading("INSPECTOR"))
        rl.addWidget(QLabel("Audio monitor volume")); self.vol=QSlider(Qt.Horizontal); self.vol.setRange(0,200); self.vol.setValue(100)
        self.vol.valueChanged.connect(lambda v:self.audioout.setVolume(v/100)); rl.addWidget(self.vol)
        rl.addWidget(QLabel("Output resolution")); self.res=QComboBox(); self.res.addItems(["1080p Full HD","4K UHD"]); rl.addWidget(self.res)
        rl.addWidget(QLabel("Frame rate")); self.fps=QComboBox(); self.fps.addItems(["24","25","30","50","60"]); rl.addWidget(self.fps)
        rl.addWidget(QLabel("Audio files imported:")); self.audio_list=QListWidget(); rl.addWidget(self.audio_list,1)
        split.addWidget(right); split.setSizes([250,900,250])
        root.addWidget(self.heading("EDITING TIMELINE — INITIAL BUILD"))
        self.timeline=QTableWidget(0,3); self.timeline.setHorizontalHeaderLabels(["Track","Clip","Media Type"])
        self.timeline.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch); self.timeline.setMinimumHeight(150); root.addWidget(self.timeline)
        self.statusBar().showMessage("Ready — import media to begin.")
    def heading(self,t):
        x=QLabel(t); x.setObjectName("section"); return x
    def theme(self):
        self.setStyleSheet("""
        QMainWindow,QWidget{background:#111923;color:#e9f0f7;font-family:'Segoe UI';font-size:10pt}
        QLabel#brand{font-size:23pt;font-weight:800;color:#f5f8fc}
        QLabel#cyan,QLabel#section{color:#58c5d8;font-weight:800}
        QPushButton{background:#263b50;border:1px solid #3e5b74;border-radius:5px;padding:8px 12px}
        QPushButton:hover{background:#34536d}
        QComboBox,QListWidget,QTableWidget{background:#0b141e;border:1px solid #34495e;padding:5px}
        QHeaderView::section{background:#1e3042;color:#9edce5;padding:6px}
        QSlider::groove:horizontal{height:6px;background:#30465a}
        QSlider::handle:horizontal{background:#55c1d2;width:13px;margin:-5px 0;border-radius:6px}
        """)
    def check_tools(self):
        ok=bool(tool("ffmpeg") and tool("ffprobe")); self.engine.setText("LOCAL ENGINE READY" if ok else "ENGINE MISSING")
        self.engine.setStyleSheet("color:#8ed3a6" if ok else "color:#ffb36b")
    def add_video(self):
        fs,_=QFileDialog.getOpenFileNames(self,"Import video","","Video (*.mp4 *.mov *.mkv *.avi *.webm *.m4v)")
        for f in fs:
            self.videos.append(f); self.media.addItem("VIDEO  |  "+Path(f).name)
            self.add_timeline("V1",f,"Video")
        if fs:self.statusBar().showMessage(f"{len(fs)} video imported.")
    def add_audio(self):
        fs,_=QFileDialog.getOpenFileNames(self,"Import audio","","Audio (*.mp3 *.wav *.m4a *.aac *.ogg *.flac)")
        for f in fs:
            self.audios.append(f); self.audio_list.addItem(Path(f).name); self.add_timeline("A1",f,"Audio")
    def add_timeline(self,track,path,kind):
        r=self.timeline.rowCount(); self.timeline.insertRow(r)
        for col,val in enumerate([track,Path(path).name,kind]): self.timeline.setItem(r,col,QTableWidgetItem(val))
    def select_media(self,row):
        if row<0 or row>=len(self.videos): return
        self.current=self.videos[row]; self.player.setSource(QUrl.fromLocalFile(self.current)); self.player.pause()
    def toggle(self):
        if self.player.playbackState()==QMediaPlayer.PlayingState:self.player.pause()
        else:self.player.play()
    def remove(self):
        row=self.media.currentRow()
        if row<0:return
        self.media.takeItem(row); self.videos.pop(row); self.player.stop(); self.current=None
    def save(self):
        f,_=QFileDialog.getSaveFileName(self,"Save project","Project.mfvs","MF Studio (*.mfvs)")
        if f:
            data={"videos":self.videos,"audios":self.audios,"layout":self.layout.currentText(),"resolution":self.res.currentText(),"fps":self.fps.currentText()}
            Path(f).write_text(json.dumps(data,indent=2),encoding="utf-8"); self.statusBar().showMessage("Project saved.")
    def open_project(self):
        f,_=QFileDialog.getOpenFileName(self,"Open project","","MF Studio (*.mfvs)")
        if not f:return
        try:
            d=json.loads(Path(f).read_text(encoding="utf-8")); self.videos=d.get("videos",[]); self.audios=d.get("audios",[])
            self.media.clear(); self.audio_list.clear(); self.timeline.setRowCount(0)
            for x in self.videos:self.media.addItem("VIDEO  |  "+Path(x).name); self.add_timeline("V1",x,"Video")
            for x in self.audios:self.audio_list.addItem(Path(x).name); self.add_timeline("A1",x,"Audio")
            self.layout.setCurrentText(d.get("layout","Single Frame")); self.res.setCurrentText(d.get("resolution","1080p Full HD")); self.fps.setCurrentText(d.get("fps","30"))
            self.statusBar().showMessage("Project loaded.")
        except Exception as e:QMessageBox.critical(self,"Project error",str(e))
    def export(self):
        if not self.videos:QMessageBox.information(self,"Export","Import a video first."); return
        ff=tool("ffmpeg")
        if not ff:QMessageBox.critical(self,"FFmpeg","Bundled FFmpeg was not found."); return
        out,_=QFileDialog.getSaveFileName(self,"Export MP4","Output.mp4","MP4 (*.mp4)")
        if not out:return
        w,h=(3840,2160) if self.res.currentIndex()==1 else (1920,1080)
        cmd=[ff,"-y","-i",self.videos[0],"-vf",f"scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2","-r",self.fps.currentText(),"-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-movflags","+faststart",out]
        self.statusBar().showMessage("Rendering MP4…")
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            p=subprocess.run(cmd,capture_output=True,text=True,creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
            if p.returncode==0:QMessageBox.information(self,"Export complete","MP4 created:
"+out)
            else:QMessageBox.critical(self,"Render error",p.stderr[-3000:])
        except Exception as e:QMessageBox.critical(self,"Export error",str(e))
        finally:QApplication.restoreOverrideCursor(); self.statusBar().showMessage("Render finished.")
def main():
    app=QApplication(sys.argv); app.setApplicationName(APP); w=Main(); w.show(); sys.exit(app.exec())
if __name__=="__main__":main()
