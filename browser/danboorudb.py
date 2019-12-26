import sqlite3

class DanbooruDB:
    def __init__(self):
        self.conn = sqlite3.connect("danbooru2018_kbr.db")
        self.conn.isolation_level = None
        self.cur = self.conn.cursor()

        self.catDict={'a':1,'c':4,'d':0,'m':5,'s':3}

    def get_tags(self):
        self.cur.execute('select name from tags limit 100')
        rows = self.cur.fetchall()
        return rows
        
    def getImageIdsForTag(self,tag_name):
        # self.cur.execute('''select image_id from imageTags 
                            # where tag_id= (select tag_id from tags where name=?)
                            # order by image_id''',tag_name)
                            
        self.cur.execute('''select image_id from images
                            where user_delete = 0 and image_id in 
                            (select image_id from imageTags where tag_id in 
                                (select tag_id from tags where name=?)
                            ) order by image_id ''', tag_name)
                            
        res = self.cur.fetchall()
        return [i[0] for i in res] # list of tuples to list of ids
        
    def getExtForImage(self, image_id):
        self.cur.execute('select file_ext from images where image_id=?', (image_id,))
        res = self.cur.fetchall()
        return res[0]
        
    def get_tags2(self, filter):
        if filter == '':
            return self.get_tags()
        self.cur.execute('select name from tags where name like ? limit 100', (filter,))
        return self.cur.fetchall()
        
    def get_tags3(self, filter, cat):
        # TODO: 'not' category
        if cat == '':
            return self.get_tags2(filter)
        params = (filter, self.catDict[cat.lower()])
        self.cur.execute('select name from tags where name like ? and category = ?', params)
        return self.cur.fetchall()
        
    def getImageIdsForTag2(self,tag_name,rating):
        if rating=='':
            return self.getImageIdsForTag(tag_name)
        params = (rating.lower(),tag_name[0])

        # annoying, this variant is faster than join
        self.cur.execute('''select image_id from images
                            where user_delete = 0 and rating=? and image_id in 
                            (select image_id from imageTags where tag_id in 
                                (select tag_id from tags where name=?)
                            ) order by image_id ''', params)
                            
        #params = (tag_name[0],rating.lower())
        # self.cur.execute('''select I.image_id from images I
                            # join imageTags IT on I.image_id=IT.image_id
                            # join tags T on IT.tag_id = T.tag_id
                            # where T.name=? and I.rating=?
                            # order by I.image_id''', 
                            # params)
        res = self.cur.fetchall()
        return [i[0] for i in res] # list of tuples to list of ids
        
    def markAsDelete(self,image_id):
        self.cur.execute('update images set user_delete=1 where image_id=?',(image_id,))
        
    def getTagsForImage(self,image_id):
        self.cur.execute('''select name from tags where tag_id in 
                            (select tag_id from imageTags where image_id=?)''',(image_id,))
        res = self.cur.fetchall()
        return [i[0] for i in res] # list of tuples to list of tags
