import sqlite3

class DanbooruDB:
    def __init__(self):
        self.conn = sqlite3.connect("danbooru2018_kbr.db")
        self.conn.isolation_level = None
        self.cur = self.conn.cursor()

        self.catDict={'a':1,'c':4,'d':0,'m':5,'s':3}

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

    def get_tags(self):
        self.cur.execute('select name from tags order by name limit 1000')
        rows = self.cur.fetchall()
        return rows
                
    def get_tags2(self, filter):
        if filter == '':
            return self.get_tags()
        self.cur.execute('select name from tags where name like ? order by name', (filter,))
        return self.cur.fetchall()
        
    def get_tags3(self, filter, cat):
        # TODO: 'not' category
        if cat == '':
            return self.get_tags2(filter)
        params = (filter, self.catDict[cat.lower()])
        self.cur.execute('select name from tags where name like ? and category = ? order by name', params)
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

    def getTagsForImage2(self,image_id):
        self.cur.execute('''select category,name from tags where tag_id in 
                            (select tag_id from imageTags where image_id=?)
                            order by category,name''',(image_id,))
        res = self.cur.fetchall()
        return res

    def getImagesForTags(self, filter1, filter2):
        # TODO rating
        # TODO category per filter
        # TODO arbitrary number of filters
        start = 'select image_id from images where user_delete=0 and image_id in '
        params = []
        tag1 = 'select image_id from imageTags where tag_id in (select tag_id from tags where name=?)'
        params.append(filter1[2])
        tag2 = ''
        op = ''
        if (filter2[2] != ''):
            tag2 = 'select image_id from imageTags where tag_id in (select tag_id from tags where name=?)'
            params.append(filter2[2])
            if (filter2[0] == 'OR'):
                op = ' UNION '
            if (filter2[0] == 'AND' or filter2[0] == ''):
                op = ' INTERSECT '
            if (filter2[1] == 'NOT'):
                op = ' EXCEPT '
        full = start + '(' + tag1 + op + tag2 + ')' + 'order by image_id'
        #print(full)
        #print(tuple(params))
        self.cur.execute(full,params)
        res = self.cur.fetchall()
        return [i[0] for i in res]
