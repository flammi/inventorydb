import sqlite3
from ean_resolve import resolve_ean, EANNotResolved

#EAN-Liste generieren
db = sqlite3.connect("test.db")
cur = db.cursor()
cur.execute("SELECT ean FROM movies")
eans = [e[0] for e in cur.fetchall()]

import pprint; pprint.pprint(eans)

for ean in eans:
    try:
        dvd_movie = resolve_ean(ean, dl_dir="images") 
        cur.execute("UPDATE movies SET title=?, artists=?, duration=?, imgfile=?, studio=?, description=? WHERE ean=?", (dvd_movie["title"], ", ".join(dvd_movie["artists"]) if "artists" in dvd_movie else None, dvd_movie["duration"], dvd_movie["imgfile"], dvd_movie["studio"], dvd_movie["description"], dvd_movie["ean"])) 
        db.commit()
        print("Updating EAN = ", ean)
    except Exception as e:
        print("EAN {} could not be resolved!".format(ean))
        print(e)
