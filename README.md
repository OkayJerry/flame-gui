<h1 align="center">FLAME-GUI</h1>
<p align="center">
Graphical User Interface for <a href="https://github.com/frib-high-level-controls/FLAME">Fast Linear Accelerator Model Engine (FLAME)</a>.
</p>

![full-window](https://user-images.githubusercontent.com/70593138/179078107-8cbdae9f-5568-45e0-993d-e4003dd80489.JPG)


## How to Install (Linux Only)
**1. Install Prerequisites**
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
**2. Clone Repositories & Initialize**
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
---
## Documentation
[Official Website](https://okayjerry.github.io/flame-gui/)

### Canvas
![canvas](https://user-images.githubusercontent.com/70593138/179066057-11835b27-46a3-43cd-8498-265e6f5dea01.jpeg)

Displays the graph of the figure model. 
#### How To Use
- Click & drag the legend to move it
- Add/Remove lines using the [Parameter Tree](#parameter-tree)
- Advanced control using the [Canvas Toolbar](#canvas-toolbar)
#### Default Colors
- ![#d62728](https://via.placeholder.com/15/d62728/d62728.png) `#d62728`
- ![#1f77b4](https://via.placeholder.com/15/1f77b4/1f77b4.png) `#1f77b4`
- ![#2ca02c](https://via.placeholder.com/15/2ca02c/2ca02c.png) `#2ca02c`
- ![#ff7f0e](https://via.placeholder.com/15/ff7f0e/ff7f0e.png) `#ff7f0e`


### Canvas Toolbar
<img src="https://user-images.githubusercontent.com/70593138/179065995-c8792319-e730-4929-a2b6-fdca37133b38.JPG" width="50%"/>

Advanced controls/commands for the [Canvas](#canvas).
#### Actions
- `Home` -- Reset to original view
- `Back` -- Back to previous view
- `Forward` -- Forward to next view
- `Pan` -- Pan throughout plot
- `Zoom` -- Zoom into plot
- `Configure plot` -- Manually configure borders/spacings
- `Select Line Color` -- Manually change the color of a line
- `Save` -- Save a screenshot of the canvas

### Color Dialog
> Accessed from the `Select Line Color` action within the [Canvas Toolbar](#canvas-toolbar)

![color](https://user-images.githubusercontent.com/70593138/180307096-684c92b4-b760-4560-bad0-30b8add2e0ad.JPG)

Helps you select a line color for the [Canvas](#canvas). 


### Element View
![element-editor](https://user-images.githubusercontent.com/70593138/179042616-fbfdb8b7-124c-465e-a787-f0106e001ddf.JPG)

#### Expanding Elements
By pressing the `▶` button found within the index column, the element belonging to that index will be expand -- bringing into the rest of its attributes into view.
#### Insert, Edit, and Remove Elements
By right-clicking the **Element View**, you will be presented with three options:
1. [Insert Element](#inserting-elements)
2. [Edit Selected Element](#editing-elements)
3. `Remove Element`


### Element Config Window
> Accessed by right-clicking the [Element View](#element-view).

![lat-config](https://user-images.githubusercontent.com/70593138/181087161-c365c0f0-f618-4875-b6fe-21cceee7435c.JPG)

Used for inserting new and editing current elements.
#### Inserting Elements
After selecting `Insert Element` from [Element View](#element-view)'s right-click menu, you will be find an element's blank template. The element that you create here will be inserted at your selected index. Choose from each element type and required attributes and default values (such as the `phi`'s value) will be filled automatically.
#### Editing Elements
After choosing `Edit Selected Element` from [Element View](#element-view)'s right-click menu, the element will be opened -- making its attributes and their associated values available for edit. *Note: element index, name, and type are unavailable for change.*


### Initial Beam State Window
> Accessed from `Edit` on the menubar.

![bmstate](https://user-images.githubusercontent.com/70593138/181087197-4ca9321f-9e28-49d8-809f-273a56b2403b.JPG)

Set values for the initial beam state using this window.
#### How To Use
- Set any values
- `Apply`


### Optimization Window
> Accessed from `Edit` on the menubar.

![optimize](https://user-images.githubusercontent.com/70593138/181087250-2c5c81a4-71b9-432b-ad46-f9f13a7b38ae.JPG)

Optimize the model using selected knobs and target location.

#### Optimization Methods
- [Nelder-Mead](https://en.wikipedia.org/wiki/Nelder%E2%80%93Mead_method)
- [Differential Evolution](https://en.wikipedia.org/wiki/Differential_evolution)

#### How To Use
1. [Select Elements](#select-element-window)
2. Set `x0` values
3. Set `Target Value` and `Weight` (in relation to other parameters)
4. `Optimize`


### Parameter Tree
<img src="https://user-images.githubusercontent.com/70593138/179061034-e22a5115-af4f-4ec6-b96c-7900a0522a2f.JPG" width="30%"/>

Used for selecting which parameters to [graph](#canvas) (limited to four). After startup, the **Parameter Tree** will be completely collapsed.
#### How To Use
- To expand a category: use the `▶` button
- To collapse a category: use the `▼` button
- To select a parameter to [graph](#canvas): use the `☐` button
- To remove a parameter from the [graph](#canvas): use the `☑` button


### Phase Space Window
> Accessed from `View` on the menubar.

![phase](https://user-images.githubusercontent.com/70593138/181087313-d18f3e4b-1678-4e21-812d-c74d5a741b56.JPG)

View the phase space plot for an element.
#### How To Use
- To select an element: use the box in the top-left
- To filter the selectable elements: use the box in the top-right


### Select Element Window
> Accessed from the [Optimization Window](#optimization-window)

![select](https://user-images.githubusercontent.com/70593138/180481452-f273d180-ca23-4f39-a7c7-c7c50ffc90a6.JPG)

Choose the knobs and target location for [optimization](#optimization-window).
#### How To Use
1. Choose from model elements any number of knobs and a target. This target must be at or beyond all knobs, otherwise your selection will be rejected and a pop-up will inform you of your error.
2. `Confirm`
---
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Credits
[@kryv](https://github.com/kryv) - directed FLAME-GUI
