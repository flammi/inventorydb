import sqlite3
import os.path
from web.webgui import app

DATABASE_FILE = "test.db"
IMAGE_FOLDER = "images"
#Check if file existing

def init_inventorydb():
    if os.path.exists(DATABASE_FILE):  
        print("Found an database on your system...")
        return


    print("No inventory database found. Creating a new one...")
    conn = sqlite3.connect("test.db")

    conn.execute("""CREATE TABLE `inventory` (
        `ean`   TEXT,
        `category`  TEXT,
        `title` TEXT,
        `artists`   TEXT,
        `author`    TEXT,
        `duration`  INT,
        `imgfile`   TEXT,
        `studio`    TEXT,
        `description`   TEXT,
        `created`   TEXT,
        `alternative_ean`   TEXT,
        `added` TEXT
    );""")

    conn.execute("""CREATE TABLE `errors` (
        `ean`   TEXT,
        `error` TEXT
    );""")

    conn.commit()

    if not os.path.exists(IMAGE_FOLDER):
        print("Creating folder for product images")
        os.mkdir(IMAGE_FOLDER)
    else:
        print("Folder for product images already there! Is that correct? I havn't done anything to it...")

init_inventorydb()
print("Starting web-ui")
app.run("0.0.0.0", debug=True)
