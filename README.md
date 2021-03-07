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
|--|--:|--|
|is_deleted|234,782|Files which are marked as 'deleted' on Danbooru|
|no_humans|56,737|Images which do not show humans|
|not-image|14,420|Files which are not images (rar, zip, swf, mpg, etc)|
|photo|10,161|Files which are photographs, not bitmaps|
|text_only_page|1,865|Images consisting solely of text|
|duplicates|20,187|Duplicated images (1)|
|**Total**|338,152||

(1) Duplicated images have been identified by calculating a 32-bit CRC on the image _pixels_. Thus any differences based on encoding (e.g. PNG vs JPG) or metadata have been eliminated. Caution is required using both "deleted" and "duplicates" as there currently isn't a clean intersection between the two sets.

### Some Numbers

**Total rows in Images table:** 4,246,898

**Total rows in Tags table:** 436,393

**Top 20 Copyright/Subject Tags**

|Subject|Count|
|--|--:|
|touhou|658,797|
|original|556,864|
|kantai_collection|374,356|
|fate_(series)|204,881|
|fate/grand_order|136,251|
|idolmaster|133,121|
|vocaloid|99,622|
|pokemon|91,042|
|idolmaster_cinderella_girls|79,203|
|azur_lane|63,111|
|pokemon_(game)|53,811|
|mahou_shoujo_madoka_magica|53,293|
|girls_und_panzer|43,807|
|love_live!|43,668|
|fire_emblem|40,827|
|precure|36,738|
|fate/stay_night|32,869|
|final_fantasy|32,288|
|idolmaster_(classic)|32,211|
|girls_frontline|32,154|

**Top 20 Character Tags**

|Character|Count|
|--|--:|
|hatsune_miku|65,991|
|hakurei_reimu|58,649|
|kirisame_marisa|55,022|
|remilia_scarlet|42,273|
|izayoi_sakuya|38,919|
|flandre_scarlet|37,165|
|alice_margatroid|29,310|
|kochiya_sanae|29,303|
|patchouli_knowledge|29,248|
|admiral_(kantai_collection)|27,728|
|artoria_pendragon_(all)|27,686|
|cirno|27,290|
|yakumo_yukari|26,888|
|konpaku_youmu|26,819|
|shameimaru_aya|23,187|
|fujiwara_no_mokou|22,211|
|hong_meiling|21,892|
|akemi_homura|21,516|
|reisen_udongein_inaba|21,179|
|komeiji_koishi|21,071|
