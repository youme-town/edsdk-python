"""Legacy build script kept for editable installs.

All metadata has moved to pyproject.toml (PEP 621). This file only defines the C++ Extension
for environments that still invoke setup.py directly (e.g. some older tooling or manual builds).
"""

import sys
from setuptools import setup, Extension

EDSDK_PATH = "dependencies"

# Platform-specific configuration
if sys.platform == "darwin":  # macOS
    libraries = []
    library_dirs = []
    extra_compile_args = [
        "-Wall",
        "-std=c++11",
        "-stdlib=libc++",  # Use libc++ standard library
        "-DDEBUG=0",
        "-D__MACOS__",  # Define macOS platform macro for EDSDK headers
    ]
    # Use rpath to find the framework relative to the installed module
    # @loader_path = directory containing the .so file
    # Going up to site-packages/edsdk, then to Framework directory
    extra_link_args = [
        "-F", f"{EDSDK_PATH}/EDSDK/Framework",
        "-framework", "EDSDK",
        "-Wl,-rpath,@loader_path/Framework",  # For bundled framework
        "-Wl,-rpath,/Library/Frameworks",  # For system-installed framework
    ]
elif sys.platform == "win32":  # Windows
    libraries = ["EDSDK"]
    library_dirs = [f"{EDSDK_PATH}/EDSDK_64/Library"]
    extra_compile_args = ["/W4", "/DDEBUG=0"]
    extra_link_args = []
else:
    raise RuntimeError(f"Unsupported platform: {sys.platform}")

extension = Extension(
    "edsdk.api",
    libraries=libraries,
    include_dirs=[f"{EDSDK_PATH}/EDSDK/Header"],
    library_dirs=library_dirs,
    depends=["edsdk/edsdk_python.h", "edsdk/edsdk_utils.h"],
    sources=["edsdk/edsdk_python.cpp", "edsdk/edsdk_utils.cpp"],
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
)


# Delegate metadata to pyproject.toml; build extension here.
setup(ext_modules=[extension])
