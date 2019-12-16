from tkinter import *
from tkinter import ttk

class FilterView(Frame):
    def __init__(self, parent, callback):
        Frame.__init__(self,parent)
        
        self.master = parent
        
        self.ratingFilter = IntVar()
        self.ratingFilter.set(0)
        self.rateBtn = Checkbutton(parent, text="Rating", variable=self.ratingFilter)
        self.rateCmb = ttk.Combobox(parent, values=["Safe","Questionable","Explicit"])
        self.rateCmb.current(0)
        
        self.tagString = StringVar()
        tagLab = Label(parent,text="Tag string")
        txtTag = Entry(parent, textvariable=self.tagString)
        
        doitBtn = Button(parent, text="Apply Filter", command=callback)
        
        tagLab.grid(column=0, row=0)
        txtTag.grid(column=0, row=1)
        self.rateBtn.grid(column=0, row=2)
        self.rateCmb.grid(column=0, row=3)
        doitBtn.grid(column=0, row=4)

    def RatingFilter(self):
        if self.ratingFilter.get() == 0:
            return ''
        return self.rateCmb.get()[0]
        
    def NameFilter(self):
        return self.tagString.get()
        