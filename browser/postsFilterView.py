from tkinter import *
from tkinter import ttk

class PostsFilter(Frame):
    def makeTagControls(self,parent,first):
        # NOTE: construction order defines tab order
        opText = StringVar()
        opCmb = ttk.Combobox(parent, values=["AND","OR"], textvariable=opText, width=4) \
                if not first else None
        notCheckVal = IntVar()
        notCheckVal.set(0)
        notCheck = Checkbutton(parent, text="NOT", variable=notCheckVal)
        tagString = StringVar()
        txtTag = Entry(parent, textvariable=tagString)
        return (notCheck,txtTag,opCmb),(notCheckVal,tagString,opText)
    
    def __init__(self, parent, callback):
        Frame.__init__(self,parent)
        self.master = parent

        self.ctrls1,self.vars1 = self.makeTagControls(parent,True)
        self.ctrls2,self.vars2 = self.makeTagControls(parent,False)
        doitBtn = Button(parent, text="Apply Filter", command=callback)
        clearBtn = Button(parent, text="Clear", command=self.wipeit)

        self.ctrls1[0].grid(column=1,row=0)
        self.ctrls1[1].grid(column=2,row=0)
        #self.ctrls1[2].grid(column=1,row=0)

        self.ctrls2[0].grid(column=1,row=1)
        self.ctrls2[1].grid(column=2,row=1)
        self.ctrls2[2].grid(column=0,row=1)

        doitBtn.grid(column=0, row=2)
        clearBtn.grid(column=2, row=2)
        
    def TagFilter1(self):
        return (self.vars1[2].get(),
                ('' if self.vars1[0].get() == 0 else "NOT"),
               self.vars1[1].get())

    def TagFilter2(self):
        return (self.vars2[2].get(),
                ('' if self.vars2[0].get() == 0 else "NOT"),
               self.vars2[1].get())

    def wipeit(self):
        self.vars1[0].set(0)
        self.vars1[1].set('')
        self.vars1[2].set('')
        self.vars2[0].set(0)
        self.vars2[1].set('')
        self.vars2[2].set('')
        
