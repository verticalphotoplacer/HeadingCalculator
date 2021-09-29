# Heading Calculator

Heading Calculator tool estimates heading angle for drone photos. 

## Installation

There are three ways to install this tool: use a [precompiled executable](#use-precompiled-executable-for-windows), run as [Python application](#use-as-python-application) or [build local executable file](#build-local-executable-file).

### Use precompiled executable for Windows

A precompiled executable is provided at [the bin directory](https://github.com/verticalphotoplacer/HeadingCalculator/tree/master/bin).
Please download to your computer and double-click to run.

### Use as Python application

Heading Calculator could be used as an Python application.
It requires <b>exifread</b> library.

```
pip install exifread
```

Then, navigate to your local heading_calculator directory and run main.py

```
cd your_path/heading_calculator
python main.py
```

### Build local executable file

[pyinstaller](https://www.pyinstaller.org/) is a recommended tool to build a local executable file.
It is recommended to build from a minimal Python environment. This will exclude unnecessary packages and create minimum size executable file.

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

3. Create specfile used in building the executable file

```
cd your_path/heading_calculator
pyinstaller --onefile main.py
```

4. Modify spec file to include all image/ui/exe/config file into the executable

    Please refers to [main.spec](https://github.com/verticalphotoplacer/HeadingCalculator/blob/master/main.spec) file.

5. Create executable

```
pyinstaller --onefile main.spec
```

## Usage

Please follow the steps in Figure 1. The heading information is updated into each photo's metadata.

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
