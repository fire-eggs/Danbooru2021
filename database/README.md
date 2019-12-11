
makedb.py

A script to create a sqlite database from the Danbooru2018 metadata files.

Inspired by:
https://github.com/jxu/danbooru2018-metadata/blob/master/read_json.py

with the following important differences:

1. The image <> tag relation is normalized, with a "crosswalk" table 
   mapping the one-to-many relationship between an image and tags.
2. Indices have been created to optimize common queries.
3. The "pools" metadata is not stored in the database. The "pools" data
   has been stored in an odd fashion which I've not yet determined how
   to parse.


dbquery.py

A helper utility to allow ad-hoc queries against the database. Stolen from
the Python docs and tweaked.

