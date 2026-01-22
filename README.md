# Text Auto-Battle Arena

A lightweight text-based auto-battler. Name your fighter, enter the arena, and rack up a win streak.

## How to Run

```bash
python3 main.py
```

## How to Play

- Enter your fighter name, then choose from the menu.
- Start battles to face stronger opponents as your win streak grows.
- View your fighter stats and skill details at any time.

## Optional: Build an EXE (Windows)

If you want a double-clickable executable, you can build one with PyInstaller:

```bash
python -m pip install pyinstaller
pyinstaller --onefile --name AutoBattle main.py
```

The executable will appear in the `dist` folder.
