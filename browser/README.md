
A "browser" for viewing images associated with tags.

Presents a list of tags. Selecting a tag will show the first image
with that tag. Can cycle through all images with that tag.

The browser is a simple Tkinter interface and may be run on any platform with Python 3 installed.

To use:
1. Edit the `IMAGES_BASE` value in `tagview.py` to the path of the image set
2. execute `python tagview.py`

### Screen Cap as of 20191211

![annotated screen cap](screencap_anno.png)

1. A list of tags to select from.
2. Shows an image which has the selected tag. The image is currently sized to the view area, preserving aspect ratio.
3. The count and position in the set of images with the selected tag.
4. Buttons to move through the set of images.

#### TODO (as of 20191211):
- view more than the first 100 tags
- filtering / searching tags
- scrollable image view (when image is very large)
- show the tag category (artist / copyright / etc)

