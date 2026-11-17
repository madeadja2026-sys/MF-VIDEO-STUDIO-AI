# MF VIDEO STUDIO AI PROFESSIONAL V4.0 — Native Windows rebuild

Branding: MADE ADJA. Visual identity: Dark Professional.

This is an initial native Windows desktop build path, separated from the existing PWA. It includes a PySide6 desktop shell, local FFmpeg/FFprobe bundling, a Windows packaging script, and an Inno Setup installer definition.

## Build
The GitHub Actions workflow `.github/workflows/build-desktop-v4.yml` runs on a Windows runner. Use Actions → Build MF VIDEO STUDIO AI Windows Installer → Run workflow. The resulting installer is uploaded as a workflow artifact.

## Implemented in this first desktop milestone
- Dark Professional native desktop interface.
- Import local video and audio files.
- Video preview/playback through Qt Multimedia.
- Layout preset selector (the selector is UI groundwork; split-screen compositing is not yet wired into export).
- Basic media/timeline list and project save/open.
- Volume control for preview monitoring.
- FFmpeg MP4 export for the first video source at 1080p or 4K.

## Not yet implemented
Real multi-source split-screen composition, free layout geometry, timeline trimming/splitting, rendered multi-track audio mixing, waveform editing, transitions, keyframes, color grading, subtitle editor, local AI models, GPU acceleration, and comprehensive Windows clean-install QA.

Do not describe this milestone as a completed professional editor until these features are implemented and tested. FFmpeg licensing notices and source obligations must be reviewed before public distribution.
