---
theme: default
---
<p align="center">
 Welcome to <b>flame-gui</b>'s official user documentation! Use the quick index below to help find the things that may interest you.
</p>

![full-window](https://user-images.githubusercontent.com/70593138/179078107-8cbdae9f-5568-45e0-993d-e4003dd80489.JPG)

# Index
## Getting Started
- [Preparing a .lat and data file]()
- [Inserting, editing, and removing model elements](#insert-edit-and-remove-elements)
- [Graphing elements](#parameter-tree)
- [Configuring initial beam state](#how-to-use-2)
- [Optimizing model](#how-to-use-1)
- [Viewing model element phase space](#viewing-model-element-phase-space)

## General
 - [Canvas](#canvas)
   - [How To Use](#how-to-use)
 - [Canvas Toolbar](#canvas-toolbar)
   - [Actions](#actions)
 - [Element View](#element-view)
   - [Expanding Elements](#expanding-elements)
   - [Insert, Edit, and Remove Elements](#insert-edit-and-remove-elements)
 - [Element Configuration Window](#element-config-window)
   - [Inserting Elements](#inserting-elements)
   - [Editing Elements](#editing-elements)
 - [Optimization Window](#optimization-window)
   - [Optimization Methods](#optimization-methods)
   - [How To Use](#how-to-use-1)
 - [Initial Beam State Window](#initial-beam-state-window)
   - [How To Use](#how-to-use-2)
 - [Parameter Tree](#parameter-tree)
   - [How To Use](#how-to-use-3)
 - [Phase Space Window](#phase-space-window)
   - [How To Use](#how-to-use-4)
 - [Select Element Window](#select-element-window)
   - [How To Use](#how-to-use-5)

---
# Documentation
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

![lat-config](https://user-images.githubusercontent.com/70593138/179055270-c81163f4-ccb8-4bf7-865d-fe528b2952c0.JPG)

Used for inserting new and editing current elements.
#### Inserting Elements
After selecting `Insert Element` from [Element View](#element-view)'s right-click menu, you will be find an element's blank template. The element that you create here will be inserted at your selected index. Choose from each element type and required attributes and default values (such as the `phi`'s value) will be filled automatically.
#### Editing Elements
After choosing `Edit Selected Element` from [Element View](#element-view)'s right-click menu, the element will be opened -- making its attributes and their associated values available for edit. *Note: element index, name, and type are unavailable for change.*


### Initial Beam State Window
> Accessed from `Edit` on the menubar.

![bmstate](https://user-images.githubusercontent.com/70593138/180307165-db4de398-a46e-493b-a349-2fe09c73710b.JPG)

Set values for the initial beam state using this window.
#### How To Use
- Set any values
- `Apply`


### Optimization Window
> Accessed from `Edit` on the menubar.

![optimize](https://user-images.githubusercontent.com/70593138/179074856-99d45297-1a48-4c3c-ae81-29042b37eebc.JPG)

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

![phase](https://user-images.githubusercontent.com/70593138/179078891-05c49e81-c019-41a3-82e2-03cad5b46f31.JPG)

View the phase space plot for an element.
#### How To Use
- To select an element: use the box in the top-left
- To filter the selectable elements: use the box in the top-right


### Select Element Window
> Accessed from the [Optimization Window](#optimization-window)

![select](https://user-images.githubusercontent.com/70593138/180307236-cbb7f815-6ef4-4835-a38e-73f99dce5546.JPG)

Choose the knobs and target location for [optimization](#optimization-window).
#### How To Use
1. Choose from model elements any number of knobs and a target. This target must be at or beyond all knobs, otherwise your selection will be rejected and a pop-up will inform you of your error.
2. `Confirm`
