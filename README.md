# Solace Pro Funscript Player

Linux video and Funscript player for the Lovense Solace Pro with direct Bluetooth Low Energy (BLE) control, without Intiface.

## Current release

**v1.1.0 — BLE Direct**

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
- Linux desktop GUI

## Requirements

- Linux
- Python 3
- Bluetooth Low Energy
- MPV
- Lovense Solace Pro

## Run

```bash
python3 src/Solace-Pro-Funscript-Player.py
```

The application expects its configured Python environment and uses an included direct-BLE engine.

## License

MIT License. See `LICENSE`.
