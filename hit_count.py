import os, sqlite3, re

fh = open('logfile.txt','r')

db = sqlite3.connect(':memory:') #create temporary SQLite database in memory

db.execute("""CREATE TABLE requests (ip TEXT,url TEXT)""")

for line in fh:
    line_split = line.split()
    if len(line_split) < 7:
        raise ValueError ("Not enough fields - need at least seven.")

    ip = line_split[0]
    url = line_split[6]

    # Check that the 'ip' variable really contains four sets of number separated by dots.
    if (re.match(r'\d+\.\d+\.\d+\.\d+', ip) == None):
        errmsg = "The value %s found in the first column was not an IP address." % ip
        raise ValueError (errmsg)

    # check that the 'url' variable contains a string starting with /
    if (url.startswith("/") == False):
        errmsg = "The value %s found in the 7th column was not a path beginning with /" % url
        raise ValueError ( errmsg )


    #if len(line_split) != 12:
    #    print (line_split)
    #    raise ValueError("Malformatted line - must have 10 fields")
    db.execute("INSERT INTO requests VALUES (?,?)",(ip,url) )

db.commit() #save data

# print what's in the database
print("\nData in the database\n")
results = db.execute("SELECT * FROM requests")
for row in results:
    print(row)

# Count hits from each IP
print ("\nNumber of hits from each IP\n")
results = db.execute("""SELECT ip, COUNT(ip) AS hits FROM requests GROUP BY ip""")
for row in results:
    print(row)

# Count hits from each IP for the particular URL '/mysidebars/newtab.html'
print("\nNumber of hits from each IP for url %s" % url)
target_url = '/mysidebars/newtab.html'
results = db.execute("""SELECT ip, COUNT(ip) AS hits FROM requests WHERE url=? GROUP BY ip""", [target_url])
for row in results:
    print(row)
