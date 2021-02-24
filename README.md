(updating for the Danbooru 2020 dataset in progress)

# Danbooru2020
Scripts and tools for working with the Danbooru2020 data set.

1. database - create a sqlite database from the metadata files.
2. browser - an interactive program to view images from the dataset, filtering by tags.

See:  https://www.gwern.net/Danbooru2020

For more details, view the readme file in each folder.

This is partly an exercise to learn more about Tk and sqlite with Python. An anime enthusiast might appreciate
using this as a private Danbooru service.

### Reducing the dataset

Depending on your application, you may wish to consider removing files from your working dataset. For instance, when performing facial recognition, many of the below categories are likely to be irrelevant.

In the `reduce` folder are lists of image-ids for the following categories (accurate for Danbooru2020):

|Category|Count|Description|
|--|--|--|
|is_deleted|234,782|Files which are marked as 'deleted' on Danbooru|
|no_humans|56,737|Images which do not show humans|
|not-image|14,420|Files which are not images (rar, zip, swf, mpg, etc)|
|photo|10,161|Files which are photographs, not bitmaps|
|text_only_page|1,865|Images consisting solely of text|
|duplicates|20,187|Duplicated images (1)|
|**Total**|338,152||

(1) Duplicated images have been identified by calculating a 32-bit CRC on the image _pixels_. Thus any differences based on encoding (e.g. PNG vs JPG) or metadata have been eliminated. Caution is required using both "deleted" and "duplicates" as there isn't a clean intersection between the two sets.
