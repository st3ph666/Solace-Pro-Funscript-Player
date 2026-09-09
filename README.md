# Solace Pro Funscript Player

Linux video and Funscript player for the Lovense Solace Pro with direct Bluetooth Low Energy (BLE) control, without Intiface.

## Current release

**v1.2.3 — Futuristic Bilingual Interface**

## What's new in v1.2.3

- New futuristic dark/cyan control interface
- Highly visible **FR / EN** language selector in the header
- French and English interface with persistent language selection
- Remembers the last selected folder and video
- Restores the last video when the application starts
- Optional per-video playback resume
- Periodic resume-position saving
- Resume position saved when playback is stopped
- Completed videos are removed from the resume-position history
- More robust atomic configuration saving
- More robust Funscript loading, including concatenated JSON blocks
- Improved media/folder controls and timeline presentation

## Features

- Direct BLE control for Lovense Solace Pro
- MPV video playback
- Funscript synchronization
- Interactive Funscript timeline
- Click/drag seeking and ±10 second controls
- Adjustable minimum and maximum positions
- Adjustable BLE responsiveness
- Motion amplification control
- Folder playlist playback
- Automatic next-video playback
- Optional deletion of completed video and matching Funscript
- Persistent per-video resume positions
- Last folder/video restoration
- French / English interface
- Futuristic Linux desktop GUI

## Requirements

- Linux
- Python 3
- Bluetooth Low Energy
- MPV
- Lovense Solace Pro

## Run

Place the current v1.2.3 Python script in the repository and run it with Python 3, for example:

```bash
python3 Solace-Pro-Funscript-Player-v1.2.3-Visible-FR-EN.py
```

The application uses an included direct-BLE engine and does not require Intiface.

## License

MIT License. See `LICENSE`.
