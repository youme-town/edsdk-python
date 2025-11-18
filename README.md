# edsdk-python

Python wrapper for Canon EOS Digital Software Development Kit, aka EDSDK.

Supported Python versions: 3.8 – 3.13 (CPython).

Supported Platforms:
- **Windows** (64-bit): Fully tested and supported
- **macOS**: Supported (requires EDSDK for macOS from Canon)

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

### For Windows:

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

### For macOS:

Unzip the macOS EDSDK package and copy the header files to the `dependencies` folder:

1. Copy `EDSDK/Header` to `dependencies/EDSDK/Header`

For the framework, you have two options:

**Option 1: Bundle with package (Recommended)**

Copy the framework to BOTH locations:
```bash
# For building (required)
cp -r /path/to/EDSDK/Framework dependencies/EDSDK/Framework

# For bundling with the package (makes it self-contained)
mkdir -p edsdk/Framework
cp -r /path/to/EDSDK/Framework/EDSDK.framework edsdk/Framework/
```

This will include the framework in your Python package, making it completely self-contained. No environment variables needed!

**Option 2: System-wide installation**

Install the framework to the system frameworks directory:
```bash
sudo cp -r /path/to/EDSDK/Framework/EDSDK.framework /Library/Frameworks/
```

Then only copy headers for building:
```bash
cp -r /path/to/EDSDK/Header dependencies/EDSDK/Header
mkdir -p dependencies/EDSDK/Framework  # Create empty dir for build
cp -r /path/to/EDSDK/Framework dependencies/EDSDK/Framework/
```

Your dependencies folder structure should look like this:

```text
dependencies/EDSDK/Header/EDSDK.h
dependencies/EDSDK/Header/EDSDKErrors.h
dependencies/EDSDK/Header/EDSDKTypes.h
dependencies/EDSDK/Framework/EDSDK.framework/  # For building

# If using Option 1, also:
edsdk/Framework/EDSDK.framework/  # Bundled with package
```


## Modify EDSDKTypes.h (Windows only)

**Note: This step is only required on Windows.**

This file contains an enum definition, called `Unknown`, which collides with a DEFINE in the `Windows.h` header.

Therefore it needs to be renamed.

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

**Important for macOS**: Make sure you have Xcode Command Line Tools installed:
```bash
xcode-select --install
```

Run (this will compile the C++ extension against your current Python, e.g. 3.13):

```bash
pip install .
```

To use example programs:
```bash
pip install .[examples]
# or
uv sync --extra examples
```

To generate a wheel (recommended for distribution / reuse):

```bash
pip install build
python -m build --wheel
```

You will find the wheel under `dist/`.

### Windows
Example: `edsdk_python-0.1.2-cp313-cp313-win_amd64.whl`

Install with:
```cmd
pip install dist\edsdk_python-0.1.2-cp313-cp313-win_amd64.whl
```

### macOS
Example: `edsdk_python-0.1.2-cp313-cp313-macosx_11_0_arm64.whl`

Install with:
```bash
pip install dist/edsdk_python-0.1.2-cp313-cp313-macosx_11_0_arm64.whl
```

**Note for macOS:** The package uses `rpath` to automatically find the framework. No environment variables needed if you:
- Bundled the framework with the package (Option 1), OR
- Installed the framework to `/Library/Frameworks/` (Option 2)

The framework will be found automatically at runtime!

## Troubleshooting

### Windows Errors

- **C2365: 'Unknown': redefinition; previous definition was 'enumerator'**
    - Follow [Modify EDSDKTypes.h](#modify-edsdktypesh-windows-only).

### macOS Errors

- **fatal error: 'map' file not found** or other C++ standard library headers missing
    - Make sure Xcode Command Line Tools are installed:
      ```bash
      xcode-select --install
      ```
    - If already installed, try resetting the path:
      ```bash
      sudo xcode-select --reset
      ```
    - Verify the SDK path is correct:
      ```bash
      xcrun --show-sdk-path
      ```

- **Framework not found at runtime**
    - Make sure you either bundled the framework (Option 1) or installed it system-wide (Option 2).
    - Check if the framework exists:
      ```bash
      # For bundled framework
      ls -la ~/.local/lib/python3.*/site-packages/edsdk/Framework/EDSDK.framework

      # For system framework
      ls -la /Library/Frameworks/EDSDK.framework
      ```

### Common Errors

- **"OpenCV (cv2) not found" when running examples**
    - Install extras: `pip install edsdk-python[examples]`
