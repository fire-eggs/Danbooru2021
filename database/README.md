### makedb.py

A script to create a sqlite database from the Danbooru2019 metadata files.

**WARNING** : the full database is about **6G** in size!

Inspired by:
https://github.com/jxu/danbooru2018-metadata/blob/master/read_json.py

with the following important differences:

- The image <> tag relation is normalized, with a "crosswalk" table 
   mapping the one-to-many relationship between an image and tags.
- Indices have been created to optimize common queries.
- A `count` column has been added to the tags table. This contains
  the number of images with that tag.
- The "pools" metadata is not stored in the database. The "pools" data
   has been stored in an odd fashion which I've not yet determined how
   to parse.
- The "favs" metadata is not stored in the database. I'm not interested
  in which images are favorites of someone else.
- A new column, `hidden` has been added to the `images` table. This
   column is used to mark an image as hidden without actually deleting
   the database row. The values are a set of bit flags:
   ```
   0 : not hidden
   1 : marked as hidden by the user
   2 : no matching file in the file set
   4 : this is a duplicate image (contents exactly match another image in the file set)
   8 : this is a duplicate image (image "effectively" matches another image in the file set).
       i.e. different only by size and/or quality level.
   16: a non-image file (zip, rar, mp4, etc) which the viewer won't handle
   ```
### dbquery.py

A helper utility to allow ad-hoc queries against the database. Stolen from
the Python docs and tweaked.

### check_exists2.py

A helper script to find discrepancies between the fileset and the metadata.
Namely, there are some images in the metadata which don't have any matching
file. Marks metadata rows with missing images as `hidden |= 2` (see above).

### The Schema

Diagram manually created via dbdiagram.io/d

![database schema](schema.png)

### Notes support

"Notes" are not part of gwern's dataset. The file `notes_table.txt` defines
a table added to the database to store `note` records from Danbooru. As of
this writing, the browser code has been updated to require this table.

