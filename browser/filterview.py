#
# Finding tags
# a) tag wildcard
# b) tag category choice
# c) list of tags
# d) select a tag -> list of images for image window
#
from tkinter import *
from tkinter import ttk
from taglist import *
from danboorudb import *

class FilterView(Frame):
    def __init__(self, parent, callback, dbptr):
        Frame.__init__(self,parent)
        
        self.master = parent
        self.db = dbptr
        self.callback = callback
        parent.minsize(200, 500)

        # Tag filter string
        self.tagString1 = StringVar()
        tagLab = Label(parent,text="Tag filter string ('%' as wildcard)")
        txtTag1 = Entry(parent, textvariable=self.tagString1)

        # Tag category
        self.catFilter = IntVar()
        self.catFilter.set(0)
        catBtn = Checkbutton(parent, text="Category", variable=self.catFilter)
        self.catText = StringVar()
        catCmb = ttk.Combobox(parent, values=["Artist","Character","Descriptive","Metadata","Series"], textvariable=self.catText)
        catCmb.current(0)

        # Tag list
        leftFrame=Frame(parent)
        self.tagList = TagList(leftFrame)
        self.tagList.bindSelect(self.onselect)
        
        doitBtn = Button(parent, text="Apply Filter", command=self.update_tags)

        tagLab.grid(column=0, row=0)
        txtTag1.grid(column=0, row=1, sticky=EW)
        catBtn.grid(column=0, row=2)
        catCmb.grid(column=0, row=3)
        doitBtn.grid(column=0, row=4)
        leftFrame.grid(column=0, row=5, sticky=NSEW)
        
        parent.rowconfigure(5, weight=1)
        parent.columnconfigure(0, minsize=150, weight=1)

        self.update_tags() # initialize tag list
        
    def RatingFilter(self):
        if self.ratingFilter.get() == 0:
            return ''
        return self.ratingText.get()[0]

    def CategoryFilter(self):
        if self.catFilter.get() == 0:
            return ''
        return self.catText.get()[0]
        
    def NameFilter(self):
        return self.tagString1.get()

    def onselect(self,evt):
        who = self.tagList.getselect()
        self.callback(who)

    def update_tags(self):
        tags = self.db.get_tags_and_counts(self.NameFilter(), self.CategoryFilter())
        self.tagList.build(tags)
        
    def minimize(self):
        self.master.withdraw()

    def restore(self):
        self.master.deiconify()
        
