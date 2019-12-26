from tkinter import *
from tkinter import ttk

class FilterView(Frame):
    def __init__(self, parent, callback):
        Frame.__init__(self,parent)
        
        self.master = parent

        # Tag category
        self.catFilter = IntVar()
        self.catFilter.set(0)
        catBtn = Checkbutton(parent, text="Category", variable=self.catFilter)
        self.catText = StringVar()
        catCmb = ttk.Combobox(parent, values=["Artist","Character","Descriptive","Metadata","Series"], textvariable=self.catText)
        catCmb.current(0)
        
        # Image rating
        self.ratingFilter = IntVar()
        self.ratingFilter.set(0)
        rateBtn = Checkbutton(parent, text="Rating", variable=self.ratingFilter)
        self.ratingText = StringVar()
        rateCmb = ttk.Combobox(parent, values=["Safe","Questionable","Explicit"], textvariable=self.ratingText)
        rateCmb.current(0)
        
        self.tagString1 = StringVar()
        tagLab = Label(parent,text="Tag string")
        txtTag1 = Entry(parent, textvariable=self.tagString1)
        
        #txtTag2 = Entry(parent, textvariable=self.tagString)
        #txtTag3 = Entry(parent, textvariable=self.tagString)
        
        
        doitBtn = Button(parent, text="Apply Filter", command=callback)
        
        tagLab.grid(column=0, row=0)
        txtTag1.grid(column=0, row=1)
        
        catBtn.grid(column=0, row=2)
        catCmb.grid(column=0, row=3)
        
        rateBtn.grid(column=0, row=4)
        rateCmb.grid(column=0, row=5)
        
        doitBtn.grid(column=0, row=6)

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
        