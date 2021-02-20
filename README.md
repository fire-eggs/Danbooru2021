(updating for the Danbooru 2020 dataset in progress)

# Danbooru2019
Scripts and tools for working with the Danbooru2019 data set.

1. database - create a sqlite database from the metadata files.
2. browser - an interactive program to view images from the dataset, filtering by tags.

See:
https://www.gwern.net/Danbooru2020

For more details, view the readme file in each folder.

This is partly an exercise to learn more about Tk and sqlite with Python. An anime enthusiast might appreciate
using this as a private Danbooru service.

### Reducing the dataset

Depending on your application, you may wish to consider removing files from your working dataset. For instance, when performing facial recognition, 
all of the below categories are likely to be irrelevant.

In the `reduce` folder are lists of image-ids for the following categories (accurate for Danbooru2020):

|Category|Count|Description|
|--|--|--|
|is_deleted|234,782|Files which are marked as 'deleted' on Danbooru|
|no_humans|56,737|Images which do not show humans|
|not-image|14,420|Files which are not images (rar, zip, swf, mpg, etc)|
|photo|10,161|Files which are photographs, not bitmaps|
|text_only_page|1,865|Images consisting solely of text|
|**Total**|317,965||


### Numbers

As of February 4, 2020, here are file counts:

|Group|Count|
|--|--|
|Visible|3,668,908|
|Missing|    12,269|
|Duplicated| 10,530|
|Non-image|  10,426|

