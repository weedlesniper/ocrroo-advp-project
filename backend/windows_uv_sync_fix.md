# Windows Python Version requirements

When installing the backend using uv sync on Windows, Python versions 3.11.x and 3.14.x may cause installation failures due to numpy build issues.

### Problem:

uv sync automatically selects Python 3.14 when available.

Python 3.14 currently has no compatible numpy wheels, leading to the error:
```bash
Failed to build numpy==2.2.6
Call to mesonpy.build_wheel failed
```

Python 3.11 is also incompatible with the numpy version required by opencv.
As a result, backend installation fails on Windows unless the correct Python version is used.

### Recommended Version

Use Python 3.13.x (e.g., 3.13.9), which successfully installs all backend dependencies.

### Fix:

1.Uninstall Python 3.14 from uv (optional, but recommended):
```bash
uv python uninstall 3.14
```


2.Install Python 3.13 (from pythoor uv):
```bash
Run: uv python install 3.13.x
```
or download manually:

1. Go to: https://www.python.org/downloads/release/python-3139/
2. scroll down to Windows installer (64-bit)
3. Download and run the installer
4. After installation, verify:
```bash
python --version
```
3.Re-run backend setup:
```bash
uv sync
```
Python Interpreter(Optional, for IDE users):
```bash
If you are using PyCharm or VS Code, make sure your project interpreter is set to Python 3.13.
If the interpreter is still set to 3.11 or 3.14, update it to avoid further backend issues.
```
### Notes

1. This issue only affects Windows.
2. Linux and macOS users do not experience this numpy build failure.
3. This limitation will disappear once official numpy wheels for Python 3.14 are released.
