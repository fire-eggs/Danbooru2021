import sqlite3

class DanbooruDB:
    def __init__(self):
        self.conn = sqlite3.connect("danbooru2018_kbr.db")
        self.conn.isolation_level = None
        self.cur = self.conn.cursor()

    def get_tags(self):
        self.cur.execute('select name from tags limit 100')
        rows = self.cur.fetchall()
        return rows
        
    def getImageIdsForTag(self,tag_name):
        self.cur.execute('''select image_id from imageTags 
                            where tag_id= (select tag_id from tags where name=?)
                            order by image_id''',tag_name)
        res = self.cur.fetchall()
        return [i[0] for i in res] # list of tuples to list of ids
        
    def getExtForImage(self, image_id):
        self.cur.execute('select file_ext from images where image_id=?', (image_id,))
        res = self.cur.fetchall()
        return res[0]
        
