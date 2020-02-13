from tkinter import *
import tkinter.font
from tkinter import ttk

class TagList(Frame):
    def __init__(self, parent):
        #self.container = container
        self.master = parent
        self.tree = None
        self.tree_columns = ("tag","count")
        self._setup_widgets()
        self._init_tree()
        
    def _setup_widgets(self):
        container = self.master

        self.tree = ttk.Treeview(container,columns=self.tree_columns, show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(container,orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(container,orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(column=0, row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')
        
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)
        
    def _init_tree(self):
        for col in self.tree_columns:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: self.sortby(self.tree, c, 0))
            self.tree.column(col, width=tkinter.font.Font().measure(col.title()))

    def clear(self):
        pass
        
    def bindSelect(self, who):
        self.tree.bind("<<TreeviewSelect>>", who)
    
    def getselect(self):
        sel = self.tree.selection()
        return self.tree.set(sel, 'tag')
        
    def build(self, tree_data):
        self.tree.delete(*self.tree.get_children())
        for item in tree_data:
            self.tree.insert('', 'end', values=item)

            # # adjust columns lengths if necessary
            # for indx, val in enumerate(item):
                # ilen = tkinter.font.Font().measure(val)
                # if self.tree.column(self.tree_columns[indx], width=None) < ilen:
                    # self.tree.column(self.tree_columns[indx], width=ilen)

    def sortby(self, tree, col, descending):
        """Sort tree contents when a column is clicked on."""
        # grab values to sort
        
        data = []
        if col == 'count':
            # sort by count, then tag
            data = [(tree.set(child,col), child, tree.set(child,'tag')) for child in tree.get_children('')]
            data.sort(key=lambda t: (int(t[0]),t[2]), reverse=descending)
        else:
            data = [(tree.set(child, col), child) for child in tree.get_children('')]
            data.sort(reverse=descending)
            
        # reorder data
        for indx, item in enumerate(data):
            tree.move(item[1], '', indx)

        # switch the heading so that it will sort in the opposite direction
        tree.heading(col,
            command=lambda col=col: self.sortby(tree, col, int(not descending)))

        