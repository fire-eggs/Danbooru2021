
A "browser" for viewing images associated with tags.

Presents a list of tags. Selecting a tag will show the first image
with that tag. Can cycle through all images with that tag.

The browser is a simple Tkinter interface and may be run on any platform with Python 3 installed. Uses the sqlite 
database as defined by the database project in this repository.

To use:
1. Edit the `IMAGES_BASE` value in `tagview.py` to the path of the image set
2. execute `python tagview.py`

### Screen Cap as of 20191226

![annotated screen cap](screencap_anno.png)

1. The filter window. This entry allows you to filter by the tag name. Wildcards are currently
   using database syntax (i.e. '%' is wildcard, not '*').
2. This entry allows you to filter tags by their category (artist, character, etc)
3. This entry allows you to filter images by their rating.
4. The list of filtered tags to select from.
5. Information about the image: the filename, and the image tags.
6. The count and position in the set of images with the selected tag; buttons to move through the set of images.
7. Shows the current image with the selected tag. The image is currently sized to the view area, preserving aspect ratio.

#### TODO (as of 20191226):
- view more than the first 100 tags
- scrollable image view (when image is very large)
- show the tag category in the list (artist / character / etc)
- the image taglist needs to be more readable, a fixed size, and with a scrollbar
- add means to "delete" an image
- more tag string filter clauses; AND / OR
- ability to filter by 'NOT'
- ability to generate a file containing the paths to all images with the selected tag
- animate GIF and APNG
