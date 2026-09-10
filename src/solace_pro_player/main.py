"""Application entry point."""

from .app import *  # noqa: F403,F401

def main() -> None:
    app = SolacePlayerGUI()
    app.mainloop()

if __name__ == "__main__":
    raise SystemExit(main())
