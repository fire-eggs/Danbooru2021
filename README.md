
# Danbooru2021
Scripts and tools for working with the Danbooru2021 data set.

1. database - create a sqlite database from the (old-style) metadata files.
2. database2021 - create a sqlite database from the new 2021 metadata files.
3. browser - an interactive program to view images from the dataset, filtering by tags or rating.

See:  https://www.gwern.net/Danbooru2021

For more details, view the readme file in each folder.

This is partly an exercise to learn more about Tk and sqlite with Python. An anime enthusiast might appreciate
using this as a private Danbooru service.

### Reducing the dataset

Depending on your application, you may wish to consider removing files from your working dataset. For instance, 
when performing facial recognition, many of the below categories are likely to be irrelevant.

In the `reduce` folder are lists of image-ids for the following categories (accurate for Danbooru2020):

|Category|Count|Description|
|--|--:|--|
|is_deleted|234,782|Files which are marked as 'deleted' on Danbooru|
|no_humans|56,737|Images which do not show humans|
|not-image|14,420|Files which are not images (rar, zip, swf, mpg, etc)|
|photo|10,161|Files which are photographs, not bitmaps|
|text_only_page|1,865|Images consisting solely of text|
|duplicates|20,187|Duplicated images (1)|
|**Total**|338,152||

(1) Duplicated images have been identified by calculating a 32-bit CRC on the image _pixels_. Thus any 
differences based on encoding (e.g. PNG vs JPG) or metadata have been eliminated. Caution is required 
using both "deleted" and "duplicates" as there currently isn't a clean intersection between the two sets.

### Some Numbers

**Total rows in Images table:** 4,878,068

**Total rows in Tags table:** 498,860

**Top 10 Copyright/Subject Tags**

|Subject|Count|
|--|--:|
|touhou|697,807|
|original|652,817|
|kantai_collection|403,165|
|fate_(series)|233,412|
|fate/grand_order|161,734|
|idolmaster|147,841|
|pokemon|125,322|
|vocaloid|106,815|
|idolmaster_cinderella_girls|85,415|
|azur_lane|81,223|

**Top 10 Artist Tags**

|Artist|Count|
|--|--:|
|hammer_(sunset_beach)|4,894|
|ebifurya|4,403|
|haruyama_kazunori|4,399|
|mizuki_hitoshi|4,210|
|kouji_(campus_life)|4,024|
|itomugi-kun|3,418|
|tani_takeshi|3,410|
|tony_taka|2,961|
|bkub|2,905|
|kanon_(kurogane_knights)|2,867|

**Top 10 Character Tags**

|Character|Count|
|--|--:|
|hatsune_miku|70,825|
|hakurei_reimu|62,161|
|kirisame_marisa|57,803|
|remilia_scarlet|43,070|
|izayoi_sakuya|40,173|
|flandre_scarlet|38,132|
|admiral_(kancolle)|32,833|
|alice_margatroid|30,696|
|kochiya_sanae|30,476|
|artoria_pendragon_(fate)|30,437|

**Top 10 Non-Touhou Character Tags**

|Character|Count|
|--|--:|
|hatsune_miku|70,825|
|admiral_(kancolle)|32,833|
|artoria_pendragon_(fate)|30,437|
|akemi_homura|22,026|
|kaname_madoka|20,808|
|kaga_(kancolle)|19,490|
|saber|16,214|
|kagamine_rin|16,038|
|jeanne_d'arc_(fate)|15,992|
|miki_sayaka|15,971|


### Some More Numbers

Charts showing posting by year of various Copyright / Subjects for Danbooru 2020. The Y-axis is per year, 2005-2020.

**Top 3 by year**

![db2020_top3_by_year](https://user-images.githubusercontent.com/9809727/128425416-54859e7e-d481-4b0a-a214-e70f5c842cf1.png)

**Next Top 5 by year**

![db2020_next5_by_year](https://user-images.githubusercontent.com/9809727/128425605-6bbb633c-07e7-46ba-817f-ebd0e2fddcef.png)

**Top 5 Dwindling Subjects**

![db2020_top5_dwindle](https://user-images.githubusercontent.com/9809727/128425657-d5898b14-d76e-456d-8362-f51b61247de0.png)

**Sample of some recently rising Subjects**

![db2020_recent_rising](https://user-images.githubusercontent.com/9809727/128425748-656bad8e-bb77-4d26-9829-ee5e0b6fcd01.png)

The data used to make these charts can be found in the `tags_by_year` folder.
