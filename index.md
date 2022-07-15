---
theme: default
---
![full-window](https://user-images.githubusercontent.com/70593138/179078107-8cbdae9f-5568-45e0-993d-e4003dd80489.JPG)

Welcome to **flame-gui**'s official user documentation! Use the quick index below to help find the things that may interest you.


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
## Canvas
![canvas](https://user-images.githubusercontent.com/70593138/179066057-11835b27-46a3-43cd-8498-265e6f5dea01.jpeg)

Displays the graph of the figure model. Found central of the main page.
### How To Use
- Click & drag the legend to move it
- Add/Remove lines using the [Parameter Tree](#parameter-tree)
- Advanced control using the [Canvas Toolbar](#canvas-toolbar)


## Canvas Toolbar
![toolbar](https://user-images.githubusercontent.com/70593138/179065995-c8792319-e730-4929-a2b6-fdca37133b38.JPG)

Advanced controls/commands for the [Canvas](#canvas). Found central of the main page.
### Actions
- `Home` -- Reset to original view
- `Back` -- Back to previous view
- `Forward` -- Forward to next view
- `Pan` -- Pan throughout plot
- `Zoom` -- Zoom into plot
- `Configure plot` -- Manually configure borders/spacings
- `Select Line Color` -- Manually change the color of a line
- `Save` -- Save a screenshot of the canvas

## Color Dialog
![color](https://user-images.githubusercontent.com/70593138/179085434-c13e0ce2-9a57-48bb-8f41-4bf3f3280d23.JPG)

Helps you select a line color for the [canvas](#canvas). Accessed from the `Select Line Color` action within the [canvas toolbar](#canvas-toolbar)


## Element View
![element-editor](https://user-images.githubusercontent.com/70593138/179042616-fbfdb8b7-124c-465e-a787-f0106e001ddf.JPG)

Located at the bottom of the main page is the **Element View**.
### Expanding Elements
By pressing the `▶` button found within the index column, the element belonging to that index will be expand -- bringing into the rest of its attributes into view.
### Insert, Edit, and Remove Elements
By right-clicking the **Element View**, you will be presented with three options:
1. [Insert Element](#inserting-elements)
2. [Edit Selected Element](#editing-elements)
3. `Remove Element`


## Element Config Window
![lat-config](https://user-images.githubusercontent.com/70593138/179055270-c81163f4-ccb8-4bf7-865d-fe528b2952c0.JPG)

Used for inserting new and editing current elements. Accessed by right-clicking the **Element View**.
### Inserting Elements
After selecting `Insert Element` from [Element View](#element-view)'s right-click menu, you will be find an element's blank template. The element that you create here will be inserted at your selected index. Choose from each element type and required attributes and default values (such as the `phi`'s value) will be filled automatically.
### Editing Elements
After choosing `Edit Selected Element` from [Element View](#element-view)'s right-click menu, the element will be opened -- making its attributes and their associated values available for edit. *Note: element index, name, and type are unavailable for change.*


## Initial Beam State Window
![bmstate](https://user-images.githubusercontent.com/70593138/179074477-5ce875df-07a1-48cd-b1d9-3776b0483e66.JPG)

Set values for the initial beam state using this window. Accessed from `Edit` on the menubar.
## How To Use
- Set any values
- `Apply`


## Optimization Window
![optimize](https://user-images.githubusercontent.com/70593138/179074856-99d45297-1a48-4c3c-ae81-29042b37eebc.JPG)

Optimize the model using selected knobs and target location. Accessed from `Edit` on the menubar.

### Optimization Methods
- [Nelder-Mead](https://en.wikipedia.org/wiki/Nelder%E2%80%93Mead_method)
- [Differential Evolution](https://en.wikipedia.org/wiki/Differential_evolution)

### How To Use
1. [Select Elements](#select-element-window)
2. Set `x0` values
3. Set `Target Value` and `Weight` (in relation to other parameters)
4. `Optimize`


## Parameter Tree
![param-tree](https://user-images.githubusercontent.com/70593138/179061034-e22a5115-af4f-4ec6-b96c-7900a0522a2f.JPG)

Used for selecting which parameters to [graph](#canvas) (limited to four). After startup, the **Parameter Tree** will be completely collapsed. Found on the main page to the right.

### How To Use
- To expand a category: use the `▶` button
- To collapse a category: use the `▼` button
- To select a parameter to [graph](#canvas): use the `☐` button
- To remove a parameter from the [graph](#canvas): use the `☑` button


## Phase Space Window
![phase](https://user-images.githubusercontent.com/70593138/179078891-05c49e81-c019-41a3-82e2-03cad5b46f31.JPG)

View the phase space plot for an element. Accessed from `View` on the menubar.
### How To Use
- To select an element: use the box in the top-left
- To filter the selectable elements: use the box in the top-right


## Select Element Window
![select](https://user-images.githubusercontent.com/70593138/179074968-f8cf59d9-5d35-4616-8537-c7d32f86ecd2.JPG)

Choose the knobs and target location for [optimization](#optimization-window).
### How To Use
1. Choose from model elements any number of knobs and a target. This target must be at or beyond all knobs, otherwise your selection will be rejected and a pop-up will inform you of your error.
2. `Confirm`
