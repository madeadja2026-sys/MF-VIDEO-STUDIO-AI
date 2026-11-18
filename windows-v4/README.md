# MF VIDEO STUDIO AI PROFESSIONAL V4.0 — clean Windows rebuild

Brand: MADE ADJA. Native Windows desktop build, independent of the existing PWA and previous desktop experiments.

The first milestone provides a dark desktop shell, local video/audio import, preview, project save/open, export settings, FFmpeg/FFprobe bundling, and an Inno Setup installer pipeline.

Important: the current milestone is not yet the finished professional editor. True multi-source split-screen rendering, freely adjustable layout geometry, multi-track audio mixing, clip trimming/splitting, transitions, keyframes, waveform editing, subtitles, color grading, and local AI models remain future implementation milestones. Do not represent those as complete until implemented and tested.

Build workflow: GitHub Actions → MF VIDEO STUDIO AI V4 Clean Windows Build. The workflow pins Python 3.11 and uses the active virtual-environment interpreter, avoiding the Windows `py -3` launcher selecting an unintended Python version.
