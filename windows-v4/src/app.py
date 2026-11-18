import json
import shutil
import subprocess
import sys
from pathlib import Path

from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QFileDialog, QMessageBox, QComboBox, QSlider,
    QSplitter, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget

APP_NAME = "MF VIDEO STUDIO AI PROFESSIONAL V4.0"


def app_root():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[1]


def bundled_tool(name):
    root = Path(getattr(sys, "_MEIPASS", app_root()))
    candidates = [root / "bin" / f"{name}.exe", app_root() / "bin" / f"{name}.exe"]
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    return shutil.which(name)


class EditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} | MADE ADJA")
        self.resize(1440, 900)
        self.setMinimumSize(1080, 700)
        self.video_files = []
        self.audio_files = []
        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.player.setAudioOutput(self.audio_output)
        self._build_ui()
        self._apply_theme()
        self._check_engine()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        header = QHBoxLayout()
        brand = QLabel("MF VIDEO STUDIO AI")
        brand.setObjectName("brand")
        header.addWidget(brand)
        subtitle = QLabel("PROFESSIONAL V4.0  /  MADE ADJA")
        subtitle.setObjectName("accent")
        header.addWidget(subtitle)
        header.addStretch()
        self.engine_label = QLabel("CHECKING ENGINE")
        header.addWidget(self.engine_label)
        root.addLayout(header)

        toolbar = QHBoxLayout()
        actions = [
            ("Import Video", self.import_videos),
            ("Import Audio", self.import_audios),
            ("Save Project", self.save_project),
            ("Open Project", self.open_project),
            ("Export MP4", self.export_video),
        ]
        for caption, callback in actions:
            button = QPushButton(caption)
            button.clicked.connect(callback)
            toolbar.addWidget(button)
        toolbar.addStretch()
        root.addLayout(toolbar)

        splitter = QSplitter(Qt.Horizontal)
        root.addWidget(splitter, 1)

        media_panel = QWidget()
        media_layout = QVBoxLayout(media_panel)
        media_layout.addWidget(self._section("MEDIA LIBRARY"))
        self.video_list = QListWidget()
        self.video_list.currentRowChanged.connect(self.preview_video)
        media_layout.addWidget(self.video_list, 1)
        self.audio_list = QListWidget()
        media_layout.addWidget(self._section("AUDIO ASSETS"))
        media_layout.addWidget(self.audio_list, 1)
        splitter.addWidget(media_panel)

        preview_panel = QWidget()
        preview_layout = QVBoxLayout(preview_panel)
        preview_header = QHBoxLayout()
        preview_header.addWidget(self._section("PROGRAM MONITOR"))
        preview_header.addStretch()
        preview_header.addWidget(QLabel("Screen layout"))
        self.layout_choice = QComboBox()
        self.layout_choice.addItems([
            "Single Frame", "2 Split - Vertical", "2 Split - Horizontal",
            "3 Split - Equal", "3 Split - Main + Two"
        ])
        preview_header.addWidget(self.layout_choice)
        preview_layout.addLayout(preview_header)

        self.preview = QVideoWidget()
        self.player.setVideoOutput(self.preview)
        preview_layout.addWidget(self.preview, 1)

        transport = QHBoxLayout()
        play_button = QPushButton("Play / Pause")
        play_button.clicked.connect(self.toggle_playback)
        transport.addWidget(play_button)
        self.seek_slider = QSlider(Qt.Horizontal)
        self.seek_slider.setRange(0, 0)
        self.seek_slider.sliderMoved.connect(self.player.setPosition)
        self.player.positionChanged.connect(self.seek_slider.setValue)
        self.player.durationChanged.connect(lambda value: self.seek_slider.setRange(0, value))
        transport.addWidget(self.seek_slider, 1)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(80)
        self.volume_slider.valueChanged.connect(
            lambda value: self.audio_output.setVolume(value / 100.0)
        )
        transport.addWidget(QLabel("Monitor volume"))
        transport.addWidget(self.volume_slider)
        preview_layout.addLayout(transport)
        splitter.addWidget(preview_panel)

        inspector = QWidget()
        inspector_layout = QVBoxLayout(inspector)
        inspector_layout.addWidget(self._section("EXPORT SETTINGS"))
        inspector_layout.addWidget(QLabel("Resolution"))
        self.resolution_choice = QComboBox()
        self.resolution_choice.addItems(["1080p Full HD", "4K UHD"])
        inspector_layout.addWidget(self.resolution_choice)
        inspector_layout.addWidget(QLabel("Frame rate"))
        self.fps_choice = QComboBox()
        self.fps_choice.addItems(["24", "25", "30", "50", "60"])
        inspector_layout.addWidget(self.fps_choice)
        inspector_layout.addWidget(QLabel("Video quality"))
        self.quality_choice = QComboBox()
        self.quality_choice.addItems(["High", "Very High", "Maximum"])
        inspector_layout.addWidget(self.quality_choice)
        inspector_layout.addStretch()
        splitter.addWidget(inspector)
        splitter.setSizes([260, 900, 250])

        root.addWidget(self._section("MULTI-TRACK TIMELINE"))
        self.timeline = QTableWidget(0, 3)
        self.timeline.setHorizontalHeaderLabels(["Track", "Media", "Type"])
        self.timeline.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.timeline.setMinimumHeight(160)
        root.addWidget(self.timeline)
        self.statusBar().showMessage("Ready. Import video and audio to begin.")

    def _section(self, title):
        label = QLabel(title)
        label.setObjectName("section")
        return label

    def _apply_theme(self):
        self.setStyleSheet("""
            QMainWindow, QWidget { background:#111923; color:#eaf0f6; font-family:'Segoe UI'; font-size:10pt; }
            QLabel#brand { color:#f7fbff; font-size:23pt; font-weight:800; }
            QLabel#accent, QLabel#section { color:#59c7d8; font-weight:700; }
            QPushButton { background:#263b50; border:1px solid #405d75; border-radius:5px; padding:8px 12px; }
            QPushButton:hover { background:#34536d; }
            QComboBox, QListWidget, QTableWidget { background:#0b141e; border:1px solid #34495e; padding:5px; }
            QHeaderView::section { background:#203246; color:#c5eaf0; padding:6px; }
            QSlider::groove:horizontal { height:6px; background:#30465a; }
            QSlider::handle:horizontal { background:#59c7d8; width:13px; margin:-5px 0; border-radius:6px; }
        """)

    def _check_engine(self):
        ready = bool(bundled_tool("ffmpeg") and bundled_tool("ffprobe"))
        self.engine_label.setText("LOCAL ENGINE READY" if ready else "ENGINE NOT FOUND")
        self.engine_label.setStyleSheet("color:#8ed3a6" if ready else "color:#ffb36b")

    def _add_timeline_row(self, track, path, kind):
        row = self.timeline.rowCount()
        self.timeline.insertRow(row)
        values = [track, Path(path).name, kind]
        for column, value in enumerate(values):
            self.timeline.setItem(row, column, QTableWidgetItem(value))

    def import_videos(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Import video", "", "Video (*.mp4 *.mov *.mkv *.avi *.webm *.m4v)"
        )
        for path in paths:
            if path not in self.video_files:
                self.video_files.append(path)
                self.video_list.addItem(Path(path).name)
                self._add_timeline_row("V1", path, "Video")

    def import_audios(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Import audio", "", "Audio (*.mp3 *.wav *.m4a *.aac *.ogg *.flac)"
        )
        for path in paths:
            if path not in self.audio_files:
                self.audio_files.append(path)
                self.audio_list.addItem(Path(path).name)
                self._add_timeline_row("A1", path, "Audio")

    def preview_video(self, row):
        if 0 <= row < len(self.video_files):
            self.player.setSource(QUrl.fromLocalFile(self.video_files[row]))
            self.player.pause()

    def toggle_playback(self):
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def save_project(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save project", "Project.mfvs", "MF Video Studio Project (*.mfvs)"
        )
        if not filename:
            return
        project = {
            "videos": self.video_files,
            "audios": self.audio_files,
            "layout": self.layout_choice.currentText(),
            "resolution": self.resolution_choice.currentText(),
            "fps": self.fps_choice.currentText(),
        }
        Path(filename).write_text(json.dumps(project, indent=2), encoding="utf-8")
        self.statusBar().showMessage("Project saved.")

    def open_project(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open project", "", "MF Video Studio Project (*.mfvs)"
        )
        if not filename:
            return
        try:
            project = json.loads(Path(filename).read_text(encoding="utf-8"))
            self.video_files = project.get("videos", [])
            self.audio_files = project.get("audios", [])
            self.video_list.clear()
            self.audio_list.clear()
            self.timeline.setRowCount(0)
            for path in self.video_files:
                self.video_list.addItem(Path(path).name)
                self._add_timeline_row("V1", path, "Video")
            for path in self.audio_files:
                self.audio_list.addItem(Path(path).name)
                self._add_timeline_row("A1", path, "Audio")
            self.layout_choice.setCurrentText(project.get("layout", "Single Frame"))
            self.resolution_choice.setCurrentText(project.get("resolution", "1080p Full HD"))
            self.fps_choice.setCurrentText(project.get("fps", "30"))
            self.statusBar().showMessage("Project loaded.")
        except (OSError, ValueError, TypeError) as error:
            QMessageBox.critical(self, "Project error", str(error))

    def export_video(self):
        if not self.video_files:
            QMessageBox.information(self, "Export", "Import at least one video first.")
            return
        ffmpeg = bundled_tool("ffmpeg")
        if not ffmpeg:
            QMessageBox.critical(self, "FFmpeg", "Bundled FFmpeg was not found.")
            return
        output, _ = QFileDialog.getSaveFileName(
            self, "Export MP4", "FinalVideo.mp4", "MP4 video (*.mp4)"
        )
        if not output:
            return
        width, height = (3840, 2160) if self.resolution_choice.currentIndex() == 1 else (1920, 1080)
        quality = {"High": "21", "Very High": "18", "Maximum": "16"}[
            self.quality_choice.currentText()
        ]
        command = [
            ffmpeg, "-y", "-i", self.video_files[0],
            "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2",
            "-r", self.fps_choice.currentText(), "-c:v", "libx264", "-preset", "medium",
            "-crf", quality, "-pix_fmt", "yuv420p", "-movflags", "+faststart", output
        ]
        self.statusBar().showMessage("Rendering video. Please wait…")
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            result = subprocess.run(
                command, capture_output=True, text=True,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
            )
            if result.returncode == 0:
                QMessageBox.information(self, "Export complete", f"MP4 created:\n{output}")
            else:
                QMessageBox.critical(self, "Render error", result.stderr[-2500:])
        except OSError as error:
            QMessageBox.critical(self, "Export error", str(error))
        finally:
            QApplication.restoreOverrideCursor()
            self.statusBar().showMessage("Render process finished.")


def main():
    application = QApplication(sys.argv)
    application.setApplicationName(APP_NAME)
    window = EditorWindow()
    window.show()
    sys.exit(application.exec())


if __name__ == "__main__":
    main()
