from PyQt5.QtWidgets import QTreeWidget, QHeaderView, QTreeWidgetItem

class TreeView(QTreeWidget):
    def __init__(self,parent):
        super(QTreeWidget,self).__init__(parent)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
 

class LatTree(TreeView):
    def __init__(self,parent):
        super(TreeView,self).__init__(parent)
        self.setColumnCount(5)
        self.setHeaderLabels(['Name','Type','Attribute','Value','Unit'])
        self.header().setSectionResizeMode(QHeaderView.Stretch)
        
    def populate(self,model):
        elements = model.get_element(name=model.get_all_names())
        #elements = elements[1:] # remove ?header?
        elements =  elements[1:] # TEMPORARY
        
        for element in elements:
            item = QTreeWidgetItem()
            for key,val in element['properties'].items():
                val = str(val)
                if key == 'name':
                    item.setText(0,val)
                elif key == 'type':
                    item.setText(1,val)
                else:
                    if item.text(2) == '': 
                        item.setText(2,key)
                        item.setText(3,val)
                    else: # children are just attribute-value-unit tuples
                        child = QTreeWidgetItem()
                        item.addChild(child)
                        child.setText(2,key)
                        child.setText(3,val)
                
            self.addTopLevelItem(item)
