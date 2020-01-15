#
# Filtering by tags
# a) tag wildcard
# b) tag category choice
# c) list of tags
# d) select a tag -> list of images for image window
#
from tkinter import *
from tkinter import ttk
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

        # Tag listbox
        leftFrame=Frame(parent)
        tagLabel = ttk.Labelframe(leftFrame, text='Tags')
        tagLabel.pack(side=TOP,expand=Y,fill=BOTH)
        self.tagList = Listbox(tagLabel, relief=SUNKEN)
        self.tagList.bind('<<ListboxSelect>>', self.onselect)
        sbar = ttk.Scrollbar(tagLabel, command=self.tagList.yview, orient=VERTICAL)
        self.tagList.configure(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        self.tagList.pack(side=LEFT, fill=BOTH, expand=Y)
        
        # Image rating
        self.ratingFilter = IntVar()
        self.ratingFilter.set(0)
        rateBtn = Checkbutton(parent, text="Rating", variable=self.ratingFilter)
        self.ratingText = StringVar()
        rateCmb = ttk.Combobox(parent, values=["Safe","Questionable","Explicit"], textvariable=self.ratingText)
        rateCmb.current(0)
                        
        doitBtn = Button(parent, text="Apply Filter", command=self.update_tags)

        
        tagLab.grid(column=0, row=0)
        txtTag1.grid(column=0, row=1, sticky=EW)
        catBtn.grid(column=0, row=2)
        catCmb.grid(column=0, row=3)
        doitBtn.grid(column=0, row=4)
        leftFrame.grid(column=0, row=5, sticky=NSEW)
        
        rateBtn.grid(column=0, row=6)
        rateCmb.grid(column=0, row=7)

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
        w = evt.widget
        blah = w.curselection()
        if blah:
            index = int(w.curselection()[0])
            value = w.get(index)
            self.callback(value)

    def update_tags(self):
        self.tagList.delete(0,END)
        tags = self.db.get_tags3(self.NameFilter(), self.CategoryFilter())
        for t in tags:
            self.tagList.insert(END,t)
        self.tagList.selection_clear(0,END)
        
