# FLAME-GUI
Graphical User Interface for [Fast Linear Accelerator Model Engine (FLAME)](https://github.com/frib-high-level-controls/FLAME).

## How to Install (Linux Only)
1. Install Prerequisites
```shell
# FLAME and flame-utils
sudo apt install libboost-dev libboost-system-dev \
  libboost-thread-dev libboost-filesystem-dev \
  libboost-regex-dev libboost-program-options-dev \
  libboost-test-dev \
  build-essential cmake bison flex cppcheck git libhdf5-dev

# PyQt5
pip3 install --user pyqt5  
sudo apt-get install python3-pyqt5  
sudo apt-get install pyqt5-dev-tools
sudo apt-get install qttools5-dev-tools

# MatPlotLib
sudo apt-get install python3-matplotlib
```
2. Clone Repositories & Initialize
```shell
cd ~/path-to-directory

# flame-gui
git clone https://github.com/OkayJerry/flame-gui.git

# FLAME
git clone https://github.com/frib-high-level-controls/FLAME.git
cd FLAME
git checkout dev
mkdir bld
cd bld
cmake ..
make
sudo make install
sudo ldconfig

# flame-utils
git clone https://github.com/frib-high-level-controls/flame-utils.git
cd flame-utils
git checkout dev
python setup.py install
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Credits
[@kryv](https://github.com/kryv) - directed FLAME-GUI
