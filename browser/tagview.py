import asyncio
import os
import tkinter as tk
from tkinter import *
import PIL as pil
from PIL import Image,ImageTk
from danboorudb import *
from filterview import *

IMAGES_BASE = 'G:\\original\\'
image_ids = ()
image_index = 0

def onselect(evt):
    global image_ids
    global image_index
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    image_ids = db.getImageIdsForTag2(value,filterClass.RatingFilter())
    image_index = 0
    # TODO handle scenario where zero image ids
    update_image()

def clearImage(fault):
    info.config(text="")
    if fault:
        pict.config(image='', bg="#FF0000")
    else:
        pict.config(image='', bg="#FFFFFF")
        
def update_tags():
    #tags = db.get_tags2(filterClass.NameFilter())
    tags = db.get_tags3(filterClass.NameFilter(), filterClass.CategoryFilter())
    tagList.delete(0,END)
    for t in tags:
        tagList.insert(END, t)
    tagList.selection_clear(0,END)
    clearImage(False)

def update_image():
    global image_ids
    global image_index
    
    try:
        which = image_ids[image_index]
    except:
        # no images satisfy tag / filters
        clearImage(True)
        return

    ext = db.getExtForImage(which)
    tags = db.getTagsForImage(which)
    tags.sort()
    #print(','.join(tags))
    
    text0 = '{0}.{1}\n'.format(which,ext[0])
    text1 = '{0}\n'.format(','.join(tags))
    text2 = 'Image {0} of {1}'.format(image_index+1,len(image_ids) )
    info.config(text=text0 + text1 + text2)
    
    # the containing folder is the last three digits of the image id
    # e.g. image "12345678" is in folder "0678". Notice the leading zero;
    # all folder names are four digits wide with leading zeros.
    fold ='0' + str(image_ids[image_index])[-3:]
    while (len(fold) < 4):
        fold = '0' + fold
        
    imagePath = os.path.join(IMAGES_BASE, fold, str(which) + "." + ext[0])
    try:       
        im = pil.Image.open(imagePath)
        
        # resize image to output widget, preserving aspect ratio
        pw = pict.winfo_width()  - 4
        ph = pict.winfo_height() - 4
        
        #print("Pict:({0},{1})".format(pw,ph))
        iw,ih = im.size
        #print("Imag:({0},{1})".format(iw,ih))
        im2 = im
        if (iw > pw or ih > ph):
            if (iw < ih):
                newH = ph
                newW = int(pw * iw / ih)
            else:
                newW = pw
                newH = int(ph * ih / iw)
            im2 = im.resize((newW, newH))
            #print("New:({0},{1})".format(newW,newH))
        
        img = pil.ImageTk.PhotoImage(im2)
        pict.config(image=img, bg= "#000000") #, width=pw, height=ph)
        pict.image = img
    except Exception as e:
        clearImage(True)
        print(e)
        return

def nextImage():
    global image_ids
    global image_index
    image_index+=1
    if image_index >= len(image_ids):
        image_index = 0
    update_image()

def prevImage():
    global image_ids
    global image_index
    image_index-=1
    if image_index < 0:
        image_index = len(image_ids) - 1
    update_image()

def delImage():
    global image_ids
    global image_index
    try:
        which = image_ids[image_index]
    except:
        # no images satisfy tag / filters
        clearImage(True)
        return
    db.markAsDelete(which)
    nextImage()
    
def filterCall():
    # print("called")
    # print("Rating:{0}".format(filterClass.RatingFilter()))
    # print("Tag:{0}".format(filterClass.NameFilter()))
    update_tags()
    
tk_root = tk.Tk()
tk_root.title("Danbooru Tag Browser")
tk_root.minsize(600,400)

leftFrame=Frame(tk_root)
tagLabel = ttk.Labelframe(leftFrame, text='Tags')
tagLabel.pack(side=TOP,expand=Y,fill=BOTH)
tagList = Listbox(tagLabel, relief=SUNKEN)
tagList.bind('<<ListboxSelect>>', onselect)
sbar = ttk.Scrollbar(tagLabel, command=tagList.yview, orient=VERTICAL)
tagList.configure(yscrollcommand=sbar.set)
sbar.pack(side=RIGHT, fill=Y)
tagList.pack(side=LEFT, fill=BOTH, expand=Y)

info=Label(tk_root, text=' ', wraplength=145, justify=LEFT)
pict=Label(tk_root, text=' ',relief=SUNKEN)

btnPrev = Button(tk_root, text='Prev', command=prevImage)
btnNext = Button(tk_root, text='Next', command=nextImage)
btnDel  = Button(tk_root, text='Delete', command=delImage)

leftFrame.grid(row=0,column=0,sticky=NSEW,columnspan=2)
btnPrev.grid(row=2,column=0,sticky=E)
btnNext.grid(row=2,column=1,sticky=W)
btnDel.grid(row=3,column=0,sticky=W)
info.grid(row=1,column=0,columnspan=2,sticky=NSEW)
pict.grid(row=0,column=2,sticky=NSEW,rowspan=3)

tk_root.rowconfigure(0, weight=1)
tk_root.columnconfigure(0, minsize=150, weight=0)
tk_root.columnconfigure(1, weight=0)
tk_root.columnconfigure(2, weight=1)


db = DanbooruDB()
tags = db.get_tags()
tagList.delete(0,END)
for t in tags:
    tagList.insert(END, t)

filterClass = FilterView(Toplevel(), filterCall)

tk_root.mainloop()
