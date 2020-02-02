import sqlite3

con = sqlite3.connect("danbooru2019.db")
con.isolation_level = None
cur = con.cursor()

buffer = ""

print ("Enter your SQL commands to execute in sqlite3; terminated with semicolon (;)")
print ("Enter a blank line to exit.")

while True:
    line = input()
    if line == "":
        break
    buffer += line
    if sqlite3.complete_statement(buffer):
        try:
            buffer = buffer.strip()
            cur.execute(buffer)

            start = buffer.lstrip().upper()
            if (start.startswith("SELECT") or start.startswith("EXPLAIN")): # allow explain query plan
                res = cur.fetchall()
                print(res)
        except sqlite3.Error as e:
            print ("An error occurred:", e.args[0])
        buffer = ""

con.close()