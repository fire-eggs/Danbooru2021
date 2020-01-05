import asyncio
import os
import tkinter as tk
from tkinter import *
import tkinter.scrolledtext as tkst
import PIL as pil
from PIL import Image,ImageTk
from danboorudb import *
from filterview import *
from collections import defaultdict
from operator import itemgetter
from itertools import groupby

IMAGES_BASE = 'G:\\original\\'
image_ids = ()
image_index = -1

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
    #info.config(text="")
    info.delete(1.0,END)
    if fault:
        pict.config(image='', bg="#FF0000")
    else:
        pict.config(image='', bg="#FFFFFF")
        imageCount.config(text="")
    pict.image=None
        
def update_tags():
    global image_ids
    global image_index
    
    image_index = -1
    image_ids=()
    clearImage(False)
    
    #tags = db.get_tags2(filterClass.NameFilter())
    tags = db.get_tags3(filterClass.NameFilter(), filterClass.CategoryFilter())
    tagList.delete(0,END)
    for t in tags:
        tagList.insert(END, t)
    tagList.selection_clear(0,END)

def pictresize(event):
    update_image()
def formatTagGroup(tagDict, start, cat):
    text = ""
    if cat in tagDict:
        text = "\n".join(tagDict[cat]) + "\n"
    text = '\n' + start + ':\n' + text
    return text

def update_image():
    global image_ids
    global image_index
    
    if image_index < 0:
        clearImage(False)
        return
        
    try:
        which = image_ids[image_index]
    except:
        # no images satisfy tag / filters
        clearImage(True)
        return

    ext = db.getExtForImage(which)

        tags = db.getTagsForImage2(which)

        tagDict = dict((k,[v[1] for v in itr]) for k,itr in groupby(tags, itemgetter(0)))
        #print(tagDict)

        text0 = '{0}.{1}\n'.format(which,ext[0])
        text1 = formatTagGroup(tagDict,'Copyright',3) # '\nCopyright:\n' + ("\n".join(tagDict[3]) + "\n" if 3 in tagDict else "")
        text2 = formatTagGroup(tagDict, 'Artist', 1) #'\nArtist:\n' + ("\n".join(tagDict[1]) + "\n" if 1 in tagDict else "")
        text3 = formatTagGroup(tagDict, 'Characters', 4) #'\nCharacters:\n' + ("\n".join(tagDict[4]) + "\n" if 4 in tagDict else "")
        text4 = formatTagGroup(tagDict, 'Tags', 0) #'\nTags:\n' + ("\n".join(tagDict[0]) + "\n" if 0 in tagDict else "")
        text5 = formatTagGroup(tagDict, 'Meta', 5) #'\nMeta:\n' + ("\n".join(tagDict[5]) if 5 in tagDict else "")
    
    
    #tags.sort()
    #print(','.join(tags))
    
#    text0 = '{0}.{1}\n'.format(which,ext[0])
#    text1 = '{0}\n'.format(','.join(tags))
    #info.config(text=text0 + text1 + text2)
        info.delete(1.0,END)
        info.insert(1.0,text0+text1+text2+text3+text4+text5)
        icText = 'Image {0} of {1}'.format(image_index+1,len(image_ids) )
        imageCount.config(text=icText)
    
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
            if (iw > ih):
                newH = int((pw / iw) * ih)
                newW = pw
            else:
                newW = int((ph / ih) * iw)
                newH = ph
                
            im2 = im.resize((newW, newH))
            #print("New:({0},{1})".format(newW,newH))
        
        img = pil.ImageTk.PhotoImage(im2)
        pict.config(image=img, bg= "#EFF4F7") #, width=pw, height=ph)
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

#info=Label(tk_root, text=' ', wraplength=145, justify=LEFT)
info=tkst.ScrolledText(tk_root,width=30)
pict=Label(tk_root, text=' ',relief=SUNKEN)
pict.bind("<Configure>", pictresize)

imageCount=Label(tk_root,text=' ', justify=RIGHT)
btnPrev = Button(tk_root, text='Prev', command=prevImage)
btnNext = Button(tk_root, text='Next', command=nextImage)
btnDel  = Button(tk_root, text='Delete', command=delImage)

leftFrame.grid(row=0,column=0,sticky=NSEW,columnspan=2)
imageCount.grid(row=2,column=0,sticky=E)
btnPrev.grid(row=3,column=0,sticky=E)
btnNext.grid(row=3,column=1,sticky=W)
btnDel.grid(row=4,column=0,sticky=W)
info.grid(row=1,column=0,columnspan=2,sticky=NSEW)
pict.grid(row=0,column=2,sticky=NSEW,rowspan=5)

tk_root.rowconfigure(0, weight=1)
tk_root.rowconfigure(1, weight=1)
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
