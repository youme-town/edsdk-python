import os
from setuptools import setup, Extension, find_packages

package_name = "edsdk-python"
version = "0.1"

here = os.path.abspath(os.path.dirname(__file__))

try:
    with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = ""


_DEBUG = True
_DEBUG_LEVEL = 0

extra_compile_args = []
if _DEBUG:
    extra_compile_args += ["/W4", "/DDEBUG=%s" % _DEBUG_LEVEL]
else:
    extra_compile_args += ["/DNDEBUG"]


EDSDK_PATH = "dependencies"
# EDSDK_PATH = "dependencies/EDSDK_13.13.41_Win/"

extension = Extension(
    "edsdk.api",
    libraries=["EDSDK"],
    include_dirs=[os.path.join(EDSDK_PATH, "EDSDK/Header")],
    library_dirs=[os.path.join(EDSDK_PATH, "EDSDK_64/Library")],
    depends=["edsdk/edsdk_python.h", "edsdk/edsdk_utils.h"],
    sources=["edsdk/edsdk_python.cpp", "edsdk/edsdk_utils.cpp"],
    extra_compile_args=extra_compile_args,
)

setup(
    name=package_name,
    version=version,
    author="Francesco Leacche",
    author_email="francescoleacche@gmail.com",
    url="https://github.com/jiloc/edsdk-python",
    description="Python wrapper for Canon EDSKD Library",
    long_description=long_description,
    ext_modules=[extension],
    # Python 3.7 LTS 対応: pywin32 は 3.7 でも利用可能な範囲へピン留め / 3.8+ では現行バージョンを許可
    install_requires=[
        'pywin32>=228 ; platform_system=="Windows" and python_version>="3.8"',
        'pywin32>=228,<306 ; platform_system=="Windows" and python_version<"3.8"',
        # 3.7 環境安定性向上 (forward compatibility 用): typing_extensions は軽量
        'typing_extensions; python_version<"3.8"',
    ],
    extras_require={
        # ライブビュー表示や例を動かすためのオプション依存 (Python バージョン毎に分離)
        "display": [
            # 3.8 以上: 最新系
            "numpy>=1.24; python_version>='3.8'",
            "opencv-python>=4.9; python_version>='3.8'",
            "Pillow>=10.0; python_version>='3.8'",
            # 3.7: 最終対応版に近い安定バージョン (1.21 系, Pillow 9.x, opencv-python 4.5 系)
            "numpy>=1.20,<1.22; python_version<'3.8'",
            "opencv-python>=4.5,<4.6; python_version<'3.8'",
            "Pillow>=9.0,<10.0; python_version<'3.8'",
        ],
        "examples": [
            "numpy>=1.24; python_version>='3.8'",
            "opencv-python>=4.9; python_version>='3.8'",
            "Pillow>=10.0; python_version>='3.8'",
            "numpy>=1.20,<1.22; python_version<'3.8'",
            "opencv-python>=4.5,<4.6; python_version<'3.8'",
            "Pillow>=9.0,<10.0; python_version<'3.8'",
        ],
        # 開発用: Python 3.7 では互換性のある少し古いツールにピン留め
        "dev": [
            "pytest>=7.4; python_version>='3.8'",
            "mypy>=1.8; python_version>='3.8'",
            "black>=23.12; python_version>='3.8'",
            "pytest>=6.2,<7.0; python_version<'3.8'",
            "mypy>=0.991,<1.0; python_version<'3.8'",
            "black==22.12.0; python_version<'3.8'",
        ],
    },
    setup_requires=["wheel"],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "edsdk": ["py.typed", "api.pyi"],
    },
    data_files=[
        (
            "Lib/site-packages/edsdk",
            [
                EDSDK_PATH + "/EDSDK_64/Dll/EDSDK.dll",
                EDSDK_PATH + "/EDSDK_64/Dll/EdsImage.dll",
            ],
        )
    ],
    # Python 3.7 〜 3.12 を公式対応 (3.13 は未検証のため除外)
    python_requires=">=3.7,<3.13",
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Environment :: Win32 (MS Windows)",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: System :: Hardware :: Universal Serial Bus (USB)",
        "Typing :: Stubs Only",
    ],
    keywords=["edsdk", "canon"],
    license="MIT",
)
