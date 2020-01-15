import asyncio
import os
import tkinter as tk
from tkinter import *
import tkinter.scrolledtext as tkst
import PIL as pil
from PIL import Image,ImageTk
from danboorudb import *
from filterview import *
from postsFilterView import *
from collections import defaultdict
from operator import itemgetter
from itertools import groupby
from tkinter.font import Font

IMAGES_BASE = 'G:\\original\\'
image_ids = ()
image_index = -1

def clearImage(fault):
    #info.config(text="")
    info.delete(1.0,END)
    if fault:
        pict.config(image='', bg="#FF0000")
    else:
        pict.config(image='', bg="#FFFFFF")
        imageCount.config(text="")
    pict.image=None
        
def pictresize(event):
    update_image(True)

def formatTagGroup(tagDict, cat):
    text = ""
    if cat in tagDict:
        text = "\n".join(tagDict[cat]) + "\n"
    return text

def addTagGroup(info, head, text):
        info.insert(END, "\n")
        info.insert(END, head+":", ("bold",))
        info.insert(END, "\n")
        info.insert(END, text)
    
def update_image(imageOnly):
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

    if not imageOnly:
        tags = db.getTagsForImage2(which)

        # tuples of form (category,name) -> dict[category]
        tagDict = dict((k,[v[1] for v in itr]) for k,itr in groupby(tags, itemgetter(0)))

        text0 = '{0}.{1}\n'.format(which,ext[0])
        text1 = formatTagGroup(tagDict, 3)
        text2 = formatTagGroup(tagDict, 1)
        text3 = formatTagGroup(tagDict, 4)
        text4 = formatTagGroup(tagDict, 0)
        text5 = formatTagGroup(tagDict, 5)
    
        info.delete(1.0,END)
        info.insert(END, text0, ("bold",))
        addTagGroup(info, "Copyright", text1)
        addTagGroup(info, "Artist", text2)
        addTagGroup(info, "Characters", text3)
        addTagGroup(info, "Tags", text4)
        addTagGroup(info, "Meta", text5)
        
        bfont = Font(family="Helvetica", size=10, weight="bold")  # TODO make global?      
        info.tag_configure("bold", font=bfont)
        
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
        newW,newH = im.size
        #print("Imag:({0},{1})".format(iw,ih))
        im2 = im

        if (iw > pw or ih > ph):
            rw = pw / iw
            rh = ph / ih
            r =  min(rw, rh)
            newH = int(ih * r)
            newW = int(iw * r)
                    
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
    update_image(False)

def prevImage():
    global image_ids
    global image_index
    image_index-=1
    if image_index < 0:
        image_index = len(image_ids) - 1
    update_image(False)

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
    
def filterCall(tag):
    global image_ids
    global image_index
    
    image_ids = db.getImageIdsForTag2(tag,filterClass.RatingFilter())
    image_index = 0
    # TODO handle scenario where zero image ids
    update_image(False)   

def filterCall2():
    global image_ids
    global image_index
    
    image_index = -1
    image_ids=()
    clearImage(False)
    image_ids = db.getImagesForTags(postsFilter.TagFilter1(), \
                                    postsFilter.TagFilter2())
    image_index = 0
    update_image(False)    
    
tk_root = tk.Tk()
tk_root.title("Danbooru Tag Browser")
tk_root.minsize(600,400)

# Image info box
info=tkst.ScrolledText(tk_root,width=30)
pict=Label(tk_root, text=' ',relief=SUNKEN)
pict.bind("<Configure>", pictresize)

# image count and buttons
imageCount=Label(tk_root,text=' ', justify=RIGHT)
btnPrev = Button(tk_root, text='Prev', command=prevImage)
btnNext = Button(tk_root, text='Next', command=nextImage)
btnDel  = Button(tk_root, text='Delete', command=delImage)

pict.grid(row=0,column=2,sticky=NSEW,rowspan=4)
info.grid(row=0,column=0,columnspan=2,sticky=NSEW)
imageCount.grid(row=1,column=0,sticky=E)
btnPrev.grid(row=2,column=0,sticky=E)
btnNext.grid(row=2,column=1,sticky=W)
btnDel.grid(row=3,column=0,sticky=W)

tk_root.rowconfigure(0, weight=1)
tk_root.columnconfigure(0, minsize=150, weight=0)
tk_root.columnconfigure(1, weight=0)
tk_root.columnconfigure(2, weight=1)


db = DanbooruDB()
filterClass = FilterView(Toplevel(), filterCall, db)
postsFilter = PostsFilter(Toplevel(), filterCall2)

tk_root.mainloop()
