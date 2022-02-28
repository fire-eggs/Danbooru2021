import sqlite3
import json
import os
import glob

global missing_id_count

################################################################################
def import_artists(filename, connect):
  c = connect.cursor()
  
  # other_names is an list, needs to be split and go into a separate table
  
  #artist_keys=("other_names","is_deleted","is_banned","name","created_at","updated_at","group_name","id")
  
  c.execute("CREATE TABLE artists (artist_id INT PRIMARY KEY, name TEXT, is_banned INT, is_deleted INT, count INT, tag_id INT)")
  c.execute("CREATE TABLE artist_other_names (artist_id INT, name TEXT, PRIMARY KEY(artist_id,name))")
  
  with open(filename, encoding="UTF-8") as f:
    raw_json_lines = f.readlines()
    
  for raw_json_line in raw_json_lines:
    json_line = json.loads(raw_json_line)
        
    ban = int(json_line["is_banned"])
    deleted = int(json_line["is_deleted"])
    
    c.execute("INSERT OR IGNORE INTO artists VALUES (?,?,?,?,?,?)",
              (json_line["id"], json_line["name"], ban, deleted, 0, 0))
    
    if len(list(json_line["other_names"])) > 0:
      for oName in json_line["other_names"]:
        c.execute("INSERT OR IGNORE INTO artist_other_names VALUES (?,?)",
                  (json_line["id"], str(oName)))
                  
  connect.commit()
  
################################################################################
def import_tags(filename, connect):
  c = connect.cursor()
  
  #tag_keys=("name", "updated_at","is_locked","category","created_at","post_count", "id")
  
  c.execute("CREATE TABLE tags (tag_id INT PRIMARY KEY, name TEXT, category INT, count INT)")
  
  with open(filename, encoding="UTF-8") as f:
    raw_json_lines = f.readlines()
    
  for raw_json_line in raw_json_lines:
    json_line = json.loads(raw_json_line)
    
    # tags with no posts don't need to be tracked
    if (int)(json_line["post_count"]) == 0:
      continue
    
    # note the count is set to zero because 'post_count' above isn't the real count
    c.execute("INSERT OR IGNORE INTO tags VALUES (?,?,?,?)",
              (json_line["id"], json_line["name"], json_line["category"], 0))
    
  connect.commit()

################################################################################
def import_notes(filename, connect):
  c = connect.cursor()
  
  #note_keys=(body,post_id,is_active,height,version,y,x,width,created_at,updated_at,id)
  
  c.execute("CREATE TABLE notes (note_id INT PRIMARY KEY, image_id INT, body TEXT, x INT, y INT, w INT, h INT)")
  
  with open(filename, encoding="UTF-8") as f:
    raw_json_lines = f.readlines()
    
  for raw_json_line in raw_json_lines:
    json_line = json.loads(raw_json_line)

    # inactive notes don't need to be tracked    
    if (int)(json_line["is_active"]) == 0:
      continue
    
    c.execute("INSERT OR IGNORE INTO notes VALUES (?,?,?,?,?,?,?)",
              (json_line["id"], json_line["post_id"], json_line["body"], json_line["x"], json_line["y"], json_line["width"], json_line["height"]))
    
  connect.commit()

################################################################################
def import_pools(filename, connect):
  c = connect.cursor()
  
  #pool_keys=(post_count,is_deleted,description,created_at,category,post_ids,is_active,name,updated_at,id)
  
  c.execute("CREATE TABLE pools (pool_id INT PRIMARY KEY, name TEXT, desc TEXT, image_count INT)")
  c.execute("CREATE TABLE pool_images (pool_id INT, image_id INT, PRIMARY KEY(pool_id,image_id))")
  
  with open(filename, encoding="UTF-8") as f:
    raw_json_lines = f.readlines()
    
  for raw_json_line in raw_json_lines:
    json_line = json.loads(raw_json_line)

    # deleted or inactive pools don't need to be tracked
    if (int)(json_line["is_active"]) == 0 or (int)(json_line["is_deleted"]) != 0:
      continue
    
    # empty pools don't need to be tracked
    if len(json_line["post_ids"]) == 0:
      continue
      
    c.execute("INSERT OR IGNORE INTO pools VALUES (?,?,?,?)",
              (json_line["id"], json_line["name"], json_line["description"], len(json_line["post_ids"])))

    for imgId in json_line["post_ids"]:
      c.execute("INSERT OR IGNORE INTO pool_images VALUES (?,?)",
                (json_line["id"], imgId))
    
  connect.commit()

################################################################################
def create_images_tables(connect):

  c = connect.cursor()
  
  c.execute("""CREATE TABLE images (image_id INT PRIMARY KEY,rating TEXT,source TEXT,pixiv_id TEXT,
               w INT,h INT,created_at TEXT, updated_at TEXT, uploader_id INT,
               is_banned INT, is_deleted INT, is_flagged INT,
               file_ext TEXT, file_size INT, md5 TEXT,
               has_children INT, has_visible_children INT, has_active_children INT, parent_id INT)""")
               
  c.execute("CREATE TABLE itTemp (tag TEXT, cat INT, image_id INT, tag_id INT, PRIMARY KEY(tag,image_id,cat))")
  c.execute("CREATE TABLE imageTags (image_id INT, tag_id INT, PRIMARY KEY(image_id, tag_id))")
  
  connect.commit()

################################################################################
def buildImageTags(tagstring,category,pId,c):
  
    tags = tagstring.split()
    for atag in tags:
      c.execute("INSERT OR IGNORE INTO itTemp VALUES (?,?,?,?)", (atag, category, pId, 0))
  
################################################################################
def import_images(filename, connect):
  global missing_id_count
  global progress_count
    
  c = connect.cursor()
    
  with open(filename, encoding="UTF-8") as f:
    raw_json_lines = f.readlines()
    
  for raw_json_line in raw_json_lines:
    json_line = json.loads(raw_json_line)
    
    # entries with no id cannot be tracked! [banned and 'gold-only' images]
    if "id" not in json_line.keys():
      missing_id_count += 1
      continue

    pId = (int)(json_line["id"])
    
    # some keys are not found in all rows
    pixiv_id = "0"
    if "pixiv_id" in json_line.keys():
      pixiv_id = json_line["pixiv_id"]
    parent_id = "0"
    if "parent_id" in json_line.keys():
      parent_id = json_line["parent_id"]
        
    c.execute("INSERT OR IGNORE INTO images VALUES (?,?,?,?, ?,?,?,?, ?,?,?,?, ?,?,?,?, ?,?,?)",
              (pId,json_line["rating"],json_line["source"],pixiv_id,
              json_line["image_width"],json_line["image_height"],json_line["created_at"],json_line["updated_at"],
              json_line["uploader_id"],int(json_line["is_banned"]),int(json_line["is_deleted"]),int(json_line["is_flagged"]),
              json_line["file_ext"],json_line["file_size"],json_line["md5"],int(json_line["has_children"]),
              int(json_line["has_visible_children"]),int(json_line["has_active_children"]),parent_id
              ))

    buildImageTags(json_line["tag_string_character"], 4, pId, c)
    buildImageTags(json_line["tag_string_copyright"], 3, pId, c)
    buildImageTags(json_line["tag_string_meta"], 5, pId, c)
    buildImageTags(json_line["tag_string_general"], 0, pId, c)
    buildImageTags(json_line["tag_string_artist"], 1, pId, c)
    
    progress_count += 1
    if progress_count % 50000 == 0:
      print(progress_count)
      
  connect.commit()  
  
  
################################################################################
def create_indices1(connect):
  
  c = connect.cursor()
  
  # add useful indices when looking up images by tag    
  c.execute('CREATE INDEX tags_ids on tags(tag_id)')
  c.execute('CREATE INDEX tags_dex on tags(name,tag_id)')
  c.execute('CREATE INDEX image_ids on images(image_id)')
  c.execute('CREATE INDEX artist_ids on artists(artist_id)')
  c.execute('CREATE INDEX artist_tag on artists(tag_id)')
  
  # useful index for looking up image by rating
  c.execute('CREATE INDEX image_rate on images(image_id,rating)')

  connect.commit()

################################################################################
def create_indices2(connect):
  
  c = connect.cursor()
  
  c.execute('CREATE INDEX image_tags on imageTags(tag_id)')

  connect.commit()

################################################################################
def update_counts(connect):

  c = connect.cursor()
  
  c.execute("""update tags set count=
             (select count(image_id) from imagetags where imagetags.tag_id=tags.tag_id) 
              where exists 
              (select * from imagetags where imagetags.tag_id = tags.tag_id)""")
  c.execute("""update artists set count=
             (select count(image_id) from imagetags where imagetags.tag_id=artists.tag_id) 
              where exists 
              (select * from imagetags where imagetags.tag_id = artists.tag_id)""")
              
  c.execute("""UPDATE artists set tag_id=(select tag_id from tags 
               where artists.name=tags.name and tags.category=1)""")
              
  connect.commit()

################################################################################
def makeImageTags(connect):
  c = connect.cursor()
  c.execute("""update itTemp set tag_id = (select tag_id from 
               tags where tags.name=itTemp.tag and tags.category
               =itTemp.cat)""")
  c.execute("insert or ignore into imageTags select image_id,tag_id from itTemp")
  connect.commit()
  
################################################################################
if __name__ == "__main__":
  
    conn = sqlite3.connect("db2021.db")
       
    print("tags")
    import_tags("/mnt/D2/metadata/tags000000000000.json", conn)

    # posts AFTER tags to build imageTags table
    missing_id_count = 0
    progress_count = 0        
    print("posts")
    create_images_tables(conn)
    listing = glob.glob('/mnt/D2/metadata/posts*.json')
    for filename in listing:
      print(filename)
      import_images(filename, conn)

    print("entries missing id: " + str(missing_id_count))
    
    print("artists")
    import_artists("/mnt/D2/metadata/artists000000000000.json", conn)
    print("notes")
    import_notes("/mnt/D2/metadata/notes000000000000.json", conn)
    print("pools")
    import_pools("/mnt/D2/metadata/pools000000000000.json", conn)

    print("indices")   
    create_indices1(conn)
    
    print("imageTags")
    makeImageTags(conn)
    create_indices2(conn)
    
    print("counts")
    update_counts(conn)
    
    print("cleanup")
    c = conn.cursor()
    c.execute("drop table itTemp")
    c.execute("vacuum")
    
    conn.close()
    
# TODO update artist.count : number of images w/ said artist tag
# tag category=1 and tag.name = artist.name
# OR tag.name=artist_other_names.name
# [known example of the latter: 'ichijou'
#

# TODO update tags.count : number of images w/ said tag
    
# TODO artist_urls ?
# TODO tag_aliases ?
# TODO tag_implications ?
# TODO pixiv_ugoira_frame_data ?
