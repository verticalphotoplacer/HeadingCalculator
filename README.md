# Heading Calculator

Heading Calculator tool estimates heading angle for drone photos. 

## Installation

There are three ways to install this tool: use a [precompiled executable](#use-precompiled-executable-for-windows), run as [Python application](#use-as-python-application) or [build local executable file](#build-local-executable-file).

### Use precompiled executable for Windows

A precompiled executable is provided at [the bin directory](https://github.com/verticalphotoplacer/HeadingCalculator/tree/master/bin).
Please download to your computer and double-click to run.

### Use as Python application

The Heading Calculator could be used as a Python application.
It requires [exifread](https://pypi.org/project/ExifRead/) library.

```
pip install exifread
```

Download the source code of Heading Calculator to your local machine. 
Then, navigate to your local HeadingCalculator directory and run main.py.
This will open up the application user interface for use.

```
git clone https://github.com/verticalphotoplacer/HeadingCalculator.git
cd HeadingCalculator
python main.py
```

### Build local executable file

[pyinstaller](https://www.pyinstaller.org/) is a recommended tool to build a local executable file.
It is recommended to build from a minimal Python environment. This will exclude unnecessary packages and create a minimum size executable file.

1. Create and activate a virtual environment in your [Python installation](https://www.python.org/downloads/).

```
mkdir py36envtest
python -m venv venv_py36
venv_py36\Scripts>activate.bat
```

2. Install dependencies

```
pip install exifread
```

3. Install pyinstaller

```
pip install pyinstaller
```

4. Download the source code of Heading Calculator to your local machine

```
git clone https://github.com/verticalphotoplacer/HeadingCalculator.git
cd HeadingCalculator
```

5. Change the <b>pathex</b> in [main.spec](https://github.com/verticalphotoplacer/HeadingCalculator/blob/master/main.spec) file to your path

```
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
         ( 'main.ui', '.' ),
         ( 'icon/app.png', 'icon/' ),
		 ( 'icon/copypaste.png', 'icon/' ),
		 ( 'icon/erase.png', 'icon/' ),
		 ( 'icon/save2file.png', 'icon/' ),
		 ( 'tool/win/.ExifTool_config', 'tool/win/'),
         ]
		 
a = Analysis(['main.py'],
             pathex=['your_path_to_HeadingCalculator_folder'],   # change this line
             binaries=[('tool/win/exiftool.exe', 'tool/win/')],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
```

5. Create executable

```
pyinstaller --onefile main.spec
```

This will create an executable file in a new directory name <b>dist</b> (your_path/HeadingCalculator/dist)

## Usage

Please follow the steps in Figure 1. The calculated headings are visualized and shown in numbers.
The heading information is also updated into each photo's metadata.

<p align="center">
  <img align="middle" src="https://github.com/verticalphotoplacer/HeadingCalculator/blob/master/docs/hc_howtouse.PNG?raw=true" alt="Heading Calculator usage">
  <br>
  <br>
  <em><b>Figure 1. Using Heading Calculator</b></em>
</p>

## Contributing

If you find some issue that you are willing to fix, code contributions are welcome. 

## Author

* **Man Duc Chuc** 

## Credits

The author thanks the International Digital Earth Applied Science Research Center, Chubu University and National Research Institute for Earth Science and Disaster Resilience (NIED), Japan.

## License

This software is distributed under a GNU General Public License version 3.

## How to cite 
Coming soon!

## Related tools
* [Flight Separator](https://github.com/verticalphotoplacer/FlightSeparator)
* [Vertical Photo Placer Plugin](https://github.com/verticalphotoplacer/VerticalPhotoPlacer)
