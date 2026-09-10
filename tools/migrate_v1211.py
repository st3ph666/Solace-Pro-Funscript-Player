#!/usr/bin/env python3
from __future__ import annotations

import ast
import io
import re
import tokenize
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Solace-Pro-Funscript-Player-v1.2.10.py"
OLD_SRC = ROOT / "src" / "Solace-Pro-Funscript-Player.py"
PACKAGE = ROOT / "src" / "solace_pro_player"
README = ROOT / "README.md"
REQUIREMENTS = ROOT / "requirements.txt"
PYPROJECT = ROOT / "pyproject.toml"
LAUNCHER = ROOT / "Solace-Pro-Funscript-Player-v1.2.11.py"

FRENCH = re.compile(r"[àâçéèêëîïôûùüÿœ]|\b(afin|ajoute|aucun|avec|avant|choisir|commande|connexion|dossier|début|défile|écran|fichier|fenêtre|grille|lancement|lecture|même|moteur|nom|pour|priorité|retourne|script|sélection|supprime|uniquement|vidéo|lorsque|automatique|arrêt|réglage|langue|position|mouvement|lecture|démarre|charge|sauvegarde)\b", re.I)


def src(lines, node):
    end = getattr(node, "end_lineno", node.lineno)
    return "".join(lines[node.lineno - 1:end]).rstrip() + "\n"


def clean_source(source: str) -> str:
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    ranges = []
    def visit(body):
        if body and isinstance(body[0], ast.Expr):
            value = body[0].value
            if isinstance(value, ast.Constant) and isinstance(value.value, str) and FRENCH.search(value.value):
                ranges.append((body[0].lineno, body[0].end_lineno or body[0].lineno))
        for node in body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                visit(node.body)
    visit(tree.body)
    for start, end in sorted(ranges, reverse=True):
        for index in range(start - 1, end):
            lines[index] = "\n" if lines[index].endswith("\n") else ""
    text = "".join(lines)
    tokens = []
    for token in tokenize.generate_tokens(io.StringIO(text).readline):
        if token.type == tokenize.COMMENT and not token.string.startswith("#!") and FRENCH.search(token.string):
            token = tokenize.TokenInfo(token.type, "", token.start, token.end, token.line)
        tokens.append(token)
    return tokenize.untokenize(tokens)


def update_readme(text: str) -> str:
    text = text.replace("v1.2.10", "v1.2.11")
    text = text.replace("Solace-Pro-Funscript-Player-v1.2.10.py", "Solace-Pro-Funscript-Player-v1.2.11.py")
    block = '''\n## uv deployment\n\nThe recommended deployment method is [`uv`](https://docs.astral.sh/uv/). The project uses the system Python so Tkinter remains provided by the Linux distribution.\n\n### Debian / Ubuntu\n\n```bash\nsudo apt update\nsudo apt install -y python3 python3-tk mpv bluetooth bluez\n```\n\nInstall `uv` using its official installation method, then:\n\n```bash\ngit clone https://github.com/st3ph666/Solace-Pro-Funscript-Player.git\ncd Solace-Pro-Funscript-Player\nuv sync\nuv run python Solace-Pro-Funscript-Player-v1.2.11.py\n```\n\nThe direct BLE engine uses `bleak`, installed automatically by `uv sync`. Do not run `uv sync` with `sudo`.\n\n### Update\n\n```bash\ngit pull\nuv sync\nuv run python Solace-Pro-Funscript-Player-v1.2.11.py\n```\n\n## Source architecture\n\n```text\nSolace-Pro-Funscript-Player-v1.2.11.py  # Compatibility launcher\nsrc/solace_pro_player/\n├── __init__.py                         # Version metadata\n├── settings.py                         # Paths and UI constants\n├── app.py                              # Embedded BLE engine, helpers and Tkinter application\n└── main.py                             # Application entry point\n```\n\nSource-code comments are maintained in **English only**. The French / English interface remains available.\n\n'''
    if "## uv deployment" not in text:
        text += block
    return text


def main():
    source = SOURCE.read_text(encoding="utf-8")
    lines = source.splitlines(keepends=True)
    tree = ast.parse(source)
    imports = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
    constants, app_nodes = [], []
    main_node = None
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            continue
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            main_node = node
            continue
        if isinstance(node, ast.If):
            continue
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            names = [t.id for t in targets if isinstance(t, ast.Name)]
            if names and all(n.isupper() for n in names) and "ENGINE_BUNDLE" not in names and "LANGUAGE" not in names:
                constants.append(node)
                continue
        app_nodes.append(node)
    if main_node is None:
        raise RuntimeError("main() not found")

    import_text = "".join(src(lines, n) for n in imports)
    PACKAGE.mkdir(parents=True, exist_ok=True)
    settings = '"""Paths, translations, themes, and UI constants."""\n\n' + import_text + "\n" + "\n".join(src(lines, n) for n in constants)
    settings = settings.replace('APP_VERSION = "v1.2.10-TEST"', 'APP_VERSION = "v1.2.11"')
    settings = settings.replace('APP_VERSION = "v1.2.10"', 'APP_VERSION = "v1.2.11"')
    settings = re.sub(r'^PYTHON\s*=.*$', 'PYTHON = Path(sys.executable)', settings, flags=re.M)
    if "import sys" not in settings:
        settings = settings.replace("from __future__ import annotations\n", "from __future__ import annotations\nimport sys\n", 1)

    app = '"""Solace Pro application and embedded direct-BLE engine."""\n\n' + import_text + "\nfrom .settings import *  # noqa: F403,F401\n\n" + "\n".join(src(lines, n) for n in app_nodes)
    app = clean_source(app)
    main_code = '"""Application entry point."""\n\nfrom .app import *  # noqa: F403,F401\n\n' + src(lines, main_node) + '\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
    launcher = '''#!/usr/bin/env python3\n"""Compatibility launcher for Solace Pro Funscript Player v1.2.11."""\n\nfrom pathlib import Path\nimport sys\n\nROOT = Path(__file__).resolve().parent\nSRC = ROOT / "src"\nif str(SRC) not in sys.path:\n    sys.path.insert(0, str(SRC))\n\nfrom solace_pro_player.main import main\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'''

    (PACKAGE / "__init__.py").write_text('"""Solace Pro Funscript Player package."""\n\n__version__ = "1.2.11"\n', encoding="utf-8")
    (PACKAGE / "settings.py").write_text(clean_source(settings), encoding="utf-8")
    (PACKAGE / "app.py").write_text(app, encoding="utf-8")
    (PACKAGE / "main.py").write_text(main_code, encoding="utf-8")
    LAUNCHER.write_text(launcher, encoding="utf-8")
    LAUNCHER.chmod(0o755)

    REQUIREMENTS.write_text("bleak>=0.22\n", encoding="utf-8")
    PYPROJECT.write_text('''[project]\nname = "solace-pro-funscript-player"\nversion = "1.2.11"\ndescription = "Linux direct-BLE funscript player for Lovense Solace Pro"\nrequires-python = ">=3.11"\ndependencies = [\n    "bleak>=0.22",\n]\n\n[tool.uv]\npackage = false\npython-preference = "only-system"\n''', encoding="utf-8")
    README.write_text(update_readme(README.read_text(encoding="utf-8")), encoding="utf-8")
    SOURCE.unlink()
    OLD_SRC.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
