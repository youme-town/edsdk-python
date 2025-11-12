# edsdk-python

Python wrapper for Canon EOS Digital Software Development Kit, aka EDSDK.

Currently, it supports Windows only. But it shouldn't be difficult to adapt it for macOS.

## Installation and usage

### Supported Python versions (LTS)

This LTS branch targets Python **3.7 – 3.12** (CPython). Python 3.13+ is not yet validated.

If you are on Python 3.7, some optional packages require earlier pinned versions. The `setup.py` includes environment markers for this.
Examples in this README apply to any supported version unless noted.

## Quick install (core only)

```cmd
pip install edsdk-python
```

This installs only the core package and the Windows dependency (pywin32). Examples that use live view display may require extra libraries.

## Install optional dependencies for examples/display

- Via extras:

```cmd
pip install edsdk-python[display]
# or
pip install edsdk-python[examples]
```

- Or via a requirements file in this repo:

```cmd
pip install -r requirements-examples.txt
```

Typical extras include: numpy, opencv-python, Pillow.

## How to build

### 1. Create a Python 3.7 virtual environment (optional, for legacy verification)

```cmd
py -3.7 -m venv .venv
.venv\Scripts\activate
python -V  # should show 3.7.x
```

If you don't have 3.7 installed, download it from the official Python releases page.

### 2. Upgrade pip/setuptools (last versions compatible with 3.7)

```cmd
python -m pip install --upgrade "pip<24" "setuptools<70" wheel
```

### 3. Install the package

```cmd
pip install .  # or: pip install -e . for editable
```

### 4. Optional extras on Python 3.7

```cmd
pip install "numpy>=1.20,<1.22" "opencv-python>=4.5,<4.6" "Pillow>=9.0,<10.0"
```

## Obtain the EDSDK from Canon

Before you can use this library you need to obtain the EDSDK library from Canon. You can do so via their developers program:

- [Canon Europe](https://www.canon-europe.com/business/imaging-solutions/sdk/)
- [Canon Americas](https://developercommunity.usa.canon.com)
- [Canon Asia](https://asia.canon/en/campaign/developerresources)
- [Canon Oceania](https://www.canon.com.au/support/support-news/support-news/digital-slr-camera-software-developers-kit)
- [Canon China](https://www.canon.com.cn/supports/sdk/index.html)
- [Canon Korea](https://www.canon-ci.co.kr/support/sdk/sdkMain)
- [Canon Japan](https://cweb.canon.jp/eos/info/api-package/)

Once you were granted access - this may take a few days - download the latest version of their library.

## Copy the EDSDK Headers and Libraries

You should now have access to a zip file containing the file you need to build this library.

Unzip the file and copy the following folders inside the `dependencies` folder of this project:

1. `EDSDK` - Containing headers and 32-bit libraries (we only use the headers!)
2. `EDSDK_64` - Containing 64-bit version of the .lib and .dlls (which we do use!)

Your dependencies folder structure should now look like this:

```text
dependencies/EDSDK/Header/EDSDK.h
dependencies/EDSDK/Header/EDSDKErrors.h
dependencies/EDSDK/Header/EDSDKTypes.h

dependencies/EDSDK_64/Dll/EDSDK.dll
dependencies/EDSDK_64/Dll/EdsImage.dll

dependencies/EDSDK_64/Library/EDSDK.lib
```

Any additional files aren't needed, but won't hurt either in case you copied the entire folders.


## Modify EDSDKTypes.h

This file contains an enum definition, called `Unknown`, which collides with a DEFINE in the `Windows.h` header.

Therefore needs to be renamed.

```c
typedef enum
{
    Unknown   = 0x00000000,
    Jpeg      = 0x3801,
    CR2       = 0xB103,
    MP4       = 0xB982,
    CR3       = 0xB108,
    HEIF_CODE = 0xB10B,
} EdsObjectFormat;
```

You can comment out `Unknown` or rename it to `UNKNOWN` (or whatever you want) or it won't compile on Windows.


## Build the library

Run:

```cmd
pip install .
```

### Local test (smoke) after install

```cmd
python - <<"PY"
import edsdk
print("EDSDK module loaded", edsdk.__name__)
try:
    edsdk.InitializeSDK()
    print("InitializeSDK OK")
    edsdk.TerminateSDK()
    print("TerminateSDK OK")
except Exception as e:
    print("SDK init failed (likely missing DLLs / camera not connected):", e)
PY
```

If this prints `InitializeSDK OK`, the native extension loaded successfully. A connected camera is required for full functionality.

### Branch strategy (LTS vs main)

- `0.0-lts` (or similar) keeps backward compatible pins for Python 3.7.
- `main` / future feature branches can raise `python_requires` to newer versions when desired.
- Backport fixes by cherry-picking commits: `git checkout 0.0-lts && git cherry-pick <hash>`.

### Creating the LTS branch (if not already)

```cmd
git checkout -b 0.0-lts
git push -u origin 0.0-lts
```

### Release workflow for LTS

1. Adjust version in `setup.py` (e.g. `0.1.1-lts1`).
2. Build wheel:

```cmd
python -m build  # if build installed; otherwise pip install build
```

3. Test on Python 3.7 & one newer (e.g. 3.11) with smoke script.
4. Upload:

```cmd
twine upload dist/*
```

### Minimum validation checklist (Python 3.7)

| Item            | Command                                                                                                       | Expected                                   |
| --------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| Import          | `python -c "import edsdk; print('ok')"`                                                                       | ok                                         |
| List cameras    | `python -c "import edsdk; edsdk.InitializeSDK(); print('list', edsdk.GetCameraList()); edsdk.TerminateSDK()"` | Handle or empty                            |
| Capture example | `python examples\\save_image.py`                                                                              | Saves image file                           |
| Live view       | `python examples\\live_view.py --display --count 5`                                                           | 5 frames saved or window closes gracefully |

If any of these fail only on 3.7, open an issue labeled `py37`.

## Troubleshooting

If you see errors like:

- C2365: 'Unknown': redefinition; previous definition was 'enumerator'
    Follow [Modify EDSDKTypes.h](#modify-edsdktypesh).

- "OpenCV (cv2) not found" when running examples
    Install extras: `pip install edsdk-python[display]` or `pip install -r requirements-examples.txt`.

- `ModuleNotFoundError: win32api` on import (Windows only)
    Ensure `pywin32` installed inside the active environment; try `pip install --force-reinstall pywin32`.

- `EdsInitializeSDK` fails with DLL not found
    Check that `EDSDK.dll` & `EdsImage.dll` were copied into `Lib/site-packages/edsdk` by setup. If using editable install, confirm `data_files` path matches your Python installation layout.

- Build error mentioning `Unknown` enumerator
    Follow the instructions under [Modify EDSDKTypes.h](#modify-edsdktypesh). On some SDK versions this is still required.

### Reporting issues

When filing an issue for Python 3.7, include:

- Python version (`python -V`)
- Output of `pip freeze | findstr edsdk` (Windows cmd) or `pip freeze | grep edsdk`
- Minimal script, plus full traceback.

### Security note

The EDSDK runs native code. Always obtain the SDK from official Canon sources; do not trust third-party modified DLLs.
