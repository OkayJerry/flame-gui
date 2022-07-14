---
theme: default
---
![full-window](https://user-images.githubusercontent.com/70593138/179077638-50ea34cd-571c-4c3b-a363-9715c1f14ef3.JPG)

Welcome to **flame-gui**'s official user documentation! Use the quick index below to help find the things that may interest you.


# Index
## Getting Started
- [Preparing a .lat and data file](#preparing-a-lat-and-data-file)
- [Inserting, editing, and removing model elements](#insert-edit-and-remove-elements)
- [Graphing elements](#parameter-tree)
- [Using the canvas toolbar](#using-the-canvas-toolbar)
- [Configuring initial beam state](#configuring-initial-beam-state)
- [Optimizing model](#optimizing-model)
- [Viewing model element phase space](#viewing-model-element-phase-space)

## General
 - [Element View]
 - [Element Configuration Window]
 - [Parameter Tree]
 - [Canvas]
 - [Canvas Toolbar]
 - [Initial Beam State Window]
 - [Select Element Window]

---
# Documentation
## Element View
![element-editor](https://user-images.githubusercontent.com/70593138/179042616-fbfdb8b7-124c-465e-a787-f0106e001ddf.JPG)

Located at the bottom of the main page is the **Element View**.
### Expanding Elements
By pressing the `▶` button found within the index column, the element belonging to that index will be expanding -- bringing into the rest of its attributes into view.
### Insert, Edit, and Remove Elements
By right-clicking the **Element View**, you will be presented with three options:
1. [Insert Element](#inserting-elements)
2. [Edit Selected Element](#editing-elements)
3. Remove Element


## Element Config Window
![lat-config](https://user-images.githubusercontent.com/70593138/179055270-c81163f4-ccb8-4bf7-865d-fe528b2952c0.JPG)

Used for inserting new and editing current elements. Accessed by right-clicking the **Element View**.
### Inserting Elements
After selecting `Insert Element` from [Element View](#element-view)'s right-click menu, you will be find an element's blank template. The element that you create here will be inserted at your selected index. Choose from each element type and required attributes and default values (such as the `phi`'s value) will be filled automatically.
### Editing Elements
After choosing `Edit Selected Element` from [Element View](#element-view)'s right-click menu, the element will be opened -- making its attributes and their associated values available for edit. *Note: element index, name, and type are unavailable for change.*


## Parameter Tree
![param-tree](https://user-images.githubusercontent.com/70593138/179061034-e22a5115-af4f-4ec6-b96c-7900a0522a2f.JPG)

Used for selecting which parameters to [graph](#canvas) (limited to four). Found on the main page to the right.


## Canvas
![canvas](https://user-images.githubusercontent.com/70593138/179066057-11835b27-46a3-43cd-8498-265e6f5dea01.jpeg)

Displays the graph of the figure model. Found central of the main page.
### Control
- Add/Remove lines using the [Parameter Tree](#parameter-tree)
- Advanced control using the [Canvas Toolbar](#canvas-toolbar)


## Canvas Toolbar
![toolbar](https://user-images.githubusercontent.com/70593138/179065995-c8792319-e730-4929-a2b6-fdca37133b38.JPG)

Advanced controls for the [Canvas](#canvas). Found central of the main page.
### Actions
- **Home** -- Reset to original view
- **Back** -- Back to previous view
- **Forward** -- Forward to next view
- **Pan** -- Pan throughout plot
- **Zoom** -- Zoom into plot
- **Configure plot** -- Manually configure borders/spacings
- **Select Line Color** -- Manually change the color of a line
- **Save** -- Save a screenshot of the canvas


## Initial Beam State Window
![bmstate](https://user-images.githubusercontent.com/70593138/179074477-5ce875df-07a1-48cd-b1d9-3776b0483e66.JPG)

Set values for the initial beam state using this window. Accessed from `Edit` on the menubar.


## Optimization Window
![optimize](https://user-images.githubusercontent.com/70593138/179074856-99d45297-1a48-4c3c-ae81-29042b37eebc.JPG)

Optimize the model using selected knobs and target location.


## Select Element Window
![select](https://user-images.githubusercontent.com/70593138/179074968-f8cf59d9-5d35-4616-8537-c7d32f86ecd2.JPG)

Choose the knobs and target location for [optimization](#optimization-window).
