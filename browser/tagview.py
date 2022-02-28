# The "main window".
# 1. Showing the current image.
# 2. Showing information about the image: name, size, rating, and tags.
# 3. Navigation buttons
# 4. Operations buttons
#
import asyncio
import os
import tkinter as tk
from tkinter import *
import tkinter.scrolledtext as tkst
import PIL as pil
from PIL import Image,ImageTk,ImageDraw
from danboorudb import *
from filterview import *
from postsFilterView import *
from collections import defaultdict
from operator import itemgetter
from itertools import groupby
from tkinter.font import Font
from tkinter.filedialog import asksaveasfilename

import _thread, queue, time, threading
dataQueue = queue.Queue()

IMAGES_BASE = '/mnt/trollf/db2020w'
image_ids = []
image_index = -1
_last = 0
image_notes = []

master_image = None

def clearImage(fault):
    info.delete(1.0,END)
    pict.delete("all")
    noteLabel.configure(text="")
    
    if fault:
        pict.config(bg="#FF0000")
    else:
        pict.config(bg="#EFF4F7")
        imageCount.config(text="")
        
def pictresize(event):
    # picture window is being resized
    update_image(False)

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

def getFilePath(image_id, ext):

    # the containing folder is the last three digits of the image id
    # e.g. image "12345678" is in folder "0678". Notice the leading zero;
    # all folder names are four digits wide with leading zeros.
    fold ='0' + str(image_id)[-3:]
    while (len(fold) < 4):
        fold = '0' + fold
        
    imagePath = os.path.join(IMAGES_BASE, fold, str(image_id) + "." + ext)
    return imagePath
 
def showNote(text):
  # do something
  noteLabel.configure(text=text)
  pass
  
def update_image(imageOnly):
    global image_ids
    global image_index
    global master_image
    global image_notes
    
    clearImage(False)
    if image_index < 0:
        return
        
    try:
        which = image_ids[image_index]
    except:
        # no images satisfy tag / filters
        clearImage(True)
        return

    ext = db.getExtForImage(which)
    imagePath = getFilePath(image_ids[image_index], ext[0])
    if (not os.path.exists(imagePath)):
        imagePath = getFilePath(image_ids[image_index], "webp")
      
    
    # Initialize for possible image failure
    iw = 0
    ih = 0
    image_notes = []
    imageFail = False
    
    try:       
        # images in LA mode were not handled nicely [see image 715723]
        im = pil.Image.open(imagePath).convert('RGBA')
        iw,ih = im.size

        # draw note rectangles transparently on the original image [before resizing]
        # despite other suggestions, this code is what worked, see
        # https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html
        image_notes = db.getNotesForImage(which)
        if (len(image_notes) > 0):
          rect = pil.Image.new("RGBA", im.size, (255,255,255,0))
          draw = ImageDraw.Draw(rect)
          for note in image_notes:
            x = note[0]
            y = note[1]
            w = note[2]
            h = note[3]
            draw.rectangle(((x, y), (x+w, y+h)), fill=(255, 255, 0, 63))
            draw.rectangle(((x, y), (x+w, y+h)), outline=(0, 0, 0, 127), width=1)           
          out = pil.Image.alpha_composite(im, rect)
          im = out
        
        # resize image to output widget, preserving aspect ratio
        pw = pict.winfo_width()  - 4
        ph = pict.winfo_height() - 4
        
        newW,newH = im.size
        im2 = im

        if (iw > pw or ih > ph):
            rw = pw / iw
            rh = ph / ih
            r =  min(rw, rh)
            newH = int(ih * r)
            newW = int(iw * r)
            im2 = im.resize((newW, newH))
            
        # for canvas: use a global because otherwise the local copy would be garbage collected
        master_image = pil.ImageTk.PhotoImage(im2)
        
        pict.delete("all") # clear the previous image
        item = pict.create_image(2, 2, image=master_image, anchor=NW)
        
        # create rectangles on the canvas, to which we bind events to show the matching note
        # TODO 20211111 rectangles are not scaled, i.e. only correct when image is at 100%
        if (len(image_notes) > 0):
          for note in image_notes:
            x = note[0]
            y = note[1]
            w = note[2]
            h = note[3]
            t = note[4]
            n1 = pict.create_rectangle(x,y,x+w,y+h,outline='')
            pict.tag_bind(n1, "<Enter>", lambda event, t=t: showNote(t))
            pict.tag_bind(n1, "<Leave>", lambda event, t=t: showNote(""))
                    
    except Exception as e:
        print(e)
        clearImage(True)
        imageFail = True

    if not imageOnly:
        tags = db.getTagsForImage2(which)

        # tuples of form (category,name) -> dict[category]
        tagDict = dict((k,[v[1] for v in itr]) for k,itr in groupby(tags, itemgetter(0)))

        if imageFail:
          text01 = "\nFile not found"
        else:
          filesize = os.path.getsize(imagePath)
          text01 = '\nSize: {2}K ({0}x{1})'.format(iw,ih,int(filesize/1024))
          
        text0 = '{0}.{1}'.format(which,ext[0])
        text02 = '\nRating: {0}\n'.format(db.getRatingForImage(which))
        text03 = 'Notes: {0}\n'.format(str(len(image_notes)))
        
        text1 = formatTagGroup(tagDict, 3)
        text2 = formatTagGroup(tagDict, 1)
        text3 = formatTagGroup(tagDict, 4)
        text4 = formatTagGroup(tagDict, 0)
        text5 = formatTagGroup(tagDict, 5)
    
        info.delete(1.0,END)
        info.insert(END, text0, ("bold",))
        info.insert(END, text01)
        info.insert(END, text02)
        info.insert(END, text03)
        addTagGroup(info, "Copyright", text1)
        addTagGroup(info, "Artist", text2)
        addTagGroup(info, "Characters", text3)
        addTagGroup(info, "Tags", text4)
        addTagGroup(info, "Meta", text5)
        
        bfont = Font(family="Helvetica", size=10, weight="bold")  # TODO make global?
        info.tag_configure("bold", font=bfont)
        
        icText = 'Image {0} of {1}'.format(image_index+1,len(image_ids) )
        imageCount.config(text=icText)
    
def firstImage():
    global image_ids
    global image_index
    image_index = 0
    update_image(False)
    
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

def hideImage():
    global image_ids
    global image_index
    try:
        which = image_ids[image_index]
    except:
        # no images satisfy tag / filters
        clearImage(True)
        return
    db.markAsHidden(which)
    nextImage()

def makeFileList():
    global image_ids
    
    # prompt user for destination file
    # output all file paths to said file
    filetypes = [('Text', '*.txt'),('All files','*.*')]
    outfilename = asksaveasfilename(filetypes=filetypes)
    if outfilename is None or outfilename == "":
        return
    
    with open(outfilename, "w") as outfile:
        last = 0
        keepgoing = True
        while keepgoing:
            extset = db.getPagedExtForImages(image_ids,last)
            last += len(extset)
            keepgoing = len(extset) > 0
            for pair in extset:
                outfile.write(getFilePath(pair[0],pair[1]) + "\n")
    
def spinup():
    # make sure the image drive is spun up
    imagePath = os.path.join(IMAGES_BASE, "0000", "1000.png")
    im = pil.Image.open(imagePath)
    
def producer(which):
    global _last
    global _tag

    #print("Thread:{}".format(threading.current_thread().ident))

    keepgoing = True
    while keepgoing:
        # need separate db instance because it cannot be used across threads
        if (which == 1):
            image_ids = DanbooruDB().getPagedImagesForTag(_tag,postsFilter.RatingFilter(),_last)
            if len(image_ids) > 0:
                _last = image_ids[-1]
                #print("prod:", str(len(image_ids)), str(_last))
            keepgoing = len(image_ids) > 0
        if (which == 2):
            image_ids = DanbooruDB().getImagesForTags2(postsFilter.TagFilter1(), \
                                            postsFilter.TagFilter2(), \
                                            postsFilter.TagFilter3(), \
                                            postsFilter.TagFilter4(), \
                                            postsFilter.RatingFilter())
            keepgoing = False
        dataQueue.put(image_ids)        
  
# data queue consumer - looks for updates to the image_id list
# runs in separate thread so the GUI is responsive
def consumer(root):
    global image_ids
    global image_index
    
    try:
        data = dataQueue.get(block=False)
    except queue.Empty:
        pass
    else:
        #print("Cons:", str(len(data)))
        image_ids = image_ids + data
        if image_index < 0:
            # auto-show the first image on a new request
            image_index = 0
            update_image(False)
    root.after(50, consumer, root)
        
def filterCall(tag):
    global image_ids
    global image_index
    global _tag
    global _last

    # TODO Issue: multiple threads could be active - stop the existing one?
    # TODO Issue: do we have a bunch of threads dangling? [one per query]
    
    _thread.start_new_thread(spinup, ())
    image_index = -1
    image_ids=[]
    clearImage(False)
    _tag = tag
    _last = 0
    _thread.start_new_thread(producer, (1,))
    
def filterCall2():
    global image_ids
    global image_index
    global _last

    # TODO Issue: multiple threads could be active - stop the existing one?
    # TODO Issue: do we have a bunch of threads dangling? [one per query]
    
    _thread.start_new_thread(spinup, ())
    image_index = -1
    image_ids=[]
    clearImage(False)
    _last = 0
    _thread.start_new_thread(producer, (2,))

def keypress(event):
    args = event.keysym, event.keycode, event.char 
    #print("Symbol: {}, Code: {}, Char: {}".format(*args))
    if (event.keysym == 'Next'):
        nextImage()
    if (event.keysym == 'Prior'):
        prevImage()
    if (event.keysym == 'Home'):
        firstImage()

# User has minimized the window
def minEvent(event):
    if (str(event.widget) == '.'):
        if (not tk_root.winfo_viewable()):
            filterClass.minimize()
            postsFilter.minimize()

# User has restored the window
def restoreEvent(event):
    if (str(event.widget) == '.'):
        if (tk_root.winfo_viewable()):
            filterClass.restore()
            postsFilter.restore()

def onClose():
  # identify final window layouts for hard-coded usage in main
  print(tk_root.winfo_geometry())
  print(filterClass.master.winfo_geometry())
  print(postsFilter.master.winfo_geometry())
  tk_root.destroy()
  
####################################################
# Main
        
tk_root = tk.Tk()
tk_root.title("Danbooru Tag Browser")
tk_root.minsize(600,400)

# Image info box
info=tkst.ScrolledText(tk_root,width=30)

# Image canvas
pict=Canvas(tk_root,bg="white",width=400,height=400,relief=SUNKEN)
pict.bind("<Configure>", pictresize)

# A hack location to show an image note
noteLabel = Label(tk_root)

# image count and buttons
imageCount=Label(tk_root,text=' ', justify=RIGHT)
btnPrev = Button(tk_root, text='Prev', command=prevImage)
btnNext = Button(tk_root, text='Next', command=nextImage)
btnDel  = Button(tk_root, text='Hide', command=hideImage)
btnFile = Button(tk_root, text='To File', command=makeFileList)

noteLabel.grid(row=0,column=3,sticky=NW)
pict.grid(row=1,column=3,sticky=NSEW,rowspan=4)
info.grid(row=1,column=0,columnspan=3,sticky=NSEW)
imageCount.grid(row=2,column=0,sticky=E)
btnPrev.grid(row=3,column=0,sticky=E)
btnNext.grid(row=3,column=1,sticky=W)
btnDel.grid(row=4,column=0,sticky=W)
btnFile.grid(row=4,column=2,sticky=E)


tk_root.rowconfigure(1, weight=1)
tk_root.columnconfigure(0, minsize=150) # TODO take font size into account?
tk_root.columnconfigure(3, weight=1)

tk_root.bind("<Key>", keypress)
tk_root.bind("<Unmap>", minEvent)
tk_root.bind("<Map>", restoreEvent)

# Nice padding everywhere
for child in tk_root.winfo_children(): child.grid_configure(padx=3, pady=3)

tk_root.protocol("WM_DELETE_WINDOW", onClose)

db = DanbooruDB()

tl1 = Toplevel()
filterClass = FilterView(tl1, filterCall, db)

tl2 = Toplevel()
postsFilter = PostsFilter(tl2, filterCall2)

# dirty hack: a nice initial layout that works for me
tk_root.geometry('888x816+1865+698')
tl1.geometry('262x500+1599+915')
tl2.geometry('342x189+1519+695')


_tag = ''
_last = 0

consumer(tk_root)
tk_root.mainloop()
