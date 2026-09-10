"""Paths, translations, themes, and UI constants."""

from __future__ import annotations
import sys
import base64
import json
import os
import socket
import re
import tempfile
import subprocess
import zlib
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

PLAYER = Path.home() / ".cache/solace-player/solace-pro-ble-direct-engine.py"

APP_VERSION = "v1.2.11"

APP_NAME = f"Solace Funscript Player {APP_VERSION}"

PYTHON = Path(sys.executable)

CONFIG = Path.home() / ".config/solace-player-gui.json"

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".m4v"}

VIDEO_TYPES = (
    ("Vidéos", "*.mp4 *.mkv *.avi *.mov *.webm *.m4v"),
    ("Tous les fichiers", "*"),
)

COLORS = {
    "bg": "#050810",
    "panel": "#0A1020",
    "panel_alt": "#0F1830",
    "border": "#173A5E",
    "text": "#EAF8FF",
    "muted": "#78A0B8",
    "accent": "#00CFFF",
    "accent_hover": "#59E6FF",
    "success": "#35F2A1",
    "warning": "#FFC857",
    "danger": "#FF4D7D",
    "track": "#14243B",
}
