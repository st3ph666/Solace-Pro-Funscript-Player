# Solace Pro Funscript Player

Linux video and Funscript player for the Lovense Solace Pro with direct Bluetooth Low Energy (BLE) control, without Intiface.

## Current release

**v1.2.11 — Control Core UI & Live HUD**

![Solace Pro Funscript Player v1.2.11](sceenshot.png)

## What's new in v1.2.11

- Redesigned **SOLACE // CONTROL CORE** interface
- New live technical HUD with Funscript position and motion telemetry
- Live Motion Core visualization
- Current position, BLE response, amplification and active-range meters
- Improved playlist with persistent visible selection and current-video indicators
- Direct playlist item selection and playback
- Playlist folder name and video count display
- Collapsible Media Source, Motion Matrix, Playlist and Options sections
- Three selectable interface themes: Cyber Blue, Matrix Green and Purple Neon
- Improved FR / EN language controls
- Persistent last-folder and last-video restoration
- Optional per-video playback resume from the last saved position
- Interactive Funscript timeline with seek controls
- Improved use of screen space for large desktop displays

## Features

- Direct BLE control for Lovense Solace Pro
- No Intiface required
- MPV video playback and synchronization
- Local Funscript loading
- Interactive Funscript timeline
- Click/drag seeking and ±10 second controls
- Adjustable minimum and maximum positions
- Adjustable BLE responsiveness
- Motion amplification control
- Live motion and telemetry HUD
- Folder playlist playback
- Automatic next-video playback
- Optional deletion of completed video and matching Funscript
- Persistent per-video resume positions
- Last folder/video restoration
- French / English interface
- Multiple interface themes
- Futuristic Linux desktop GUI

## Requirements

- Linux
- Python 3
- Bluetooth Low Energy
- MPV
- Lovense Solace Pro

Install the Python dependencies listed in `requirements.txt`.

## Run

```bash
python3 Solace-Pro-Funscript-Player-v1.2.11.py
```

The application uses an included direct-BLE engine and does not require Intiface.

## License

MIT License. See `LICENSE`.

## uv deployment

The recommended deployment method is [`uv`](https://docs.astral.sh/uv/). The project uses the system Python so Tkinter remains provided by the Linux distribution.

### Debian / Ubuntu

```bash
sudo apt update
sudo apt install -y python3 python3-tk mpv bluetooth bluez
```

Install `uv` using its official installation method, then:

```bash
git clone https://github.com/st3ph666/Solace-Pro-Funscript-Player.git
cd Solace-Pro-Funscript-Player
uv sync
uv run python Solace-Pro-Funscript-Player-v1.2.11.py
```

The direct BLE engine uses `bleak`, installed automatically by `uv sync`. Do not run `uv sync` with `sudo`.

### Update

```bash
git pull
uv sync
uv run python Solace-Pro-Funscript-Player-v1.2.11.py
```

## Source architecture

```text
Solace-Pro-Funscript-Player-v1.2.11.py  # Compatibility launcher
src/solace_pro_player/
├── __init__.py                         # Version metadata
├── settings.py                         # Paths and UI constants
├── app.py                              # Embedded BLE engine, helpers and Tkinter application
└── main.py                             # Application entry point
```

Source-code comments are maintained in **English only**. The French / English interface remains available.

