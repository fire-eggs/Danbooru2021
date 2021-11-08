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
        self.txtTag1 = Entry(parent, textvariable=self.tagString1)

        # Tag category
        self.catFilter = IntVar()
        self.catFilter.set(0)
        catBtn = Checkbutton(parent, text="Category", variable=self.catFilter)
        self.catText = StringVar()
        catCmb = ttk.Combobox(parent, values=["Artist","Character","Descriptive","Metadata","Series"], textvariable=self.catText)
        catCmb.current(0)

        # Tag list
        listLab = Label(parent,text="Select a tag to view images")
        leftFrame=Frame(parent)
        self.tagList = TagList(leftFrame)
        self.tagList.bindSelect(self.onselect)
        
        doitBtn = Button(parent, text="Apply Filter", command=self.update_tags)
        clearBtn= Button(parent, text="Reset", command=self.clear)

        tagLab.grid(column=0, row=0, columnspan=2)
        self.txtTag1.grid(column=0, row=1, columnspan=2, sticky=EW)
        catBtn.grid(column=0, row=2, columnspan=2)
        catCmb.grid(column=0, row=3, columnspan=2)
        doitBtn.grid(column=0, row=4)
        clearBtn.grid(column=1,row=4, sticky=E)
        listLab.grid(column=0,row=5,columnspan=2)
        leftFrame.grid(column=0, row=6, columnspan=2, sticky=NSEW)
        
        parent.rowconfigure(6, weight=1)
        parent.columnconfigure(0, minsize=100, weight=1)
        parent.columnconfigure(1, minsize=50)

        # Nice padding everywhere
        for child in parent.winfo_children(): child.grid_configure(padx=3, pady=3)

        self.txtTag1.focus_set()
        self.update_tags() # initialize tag list
        
    def RatingFilter(self):
    # rating controls removed: re-instate?
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
        
    def clear(self):
        self.catFilter.set(0)
        self.catText.set("Artist")
        self.tagString1.set("")
        self.txtTag1.focus_set()
        self.update_tags()
        
