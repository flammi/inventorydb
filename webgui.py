from flask import Flask, render_template, request
app = Flask(__name__)
import sqlite3

from ean_resolve import resolve_ean

@app.route("/")
def main():
    DB = sqlite3.connect("test.db")
    DB.row_factory = sqlite3.Row
    cur = DB.cursor()
    cur.execute("SELECT ean, title, imgfile, duration FROM movies WHERE title IS NOT NULL ORDER BY title ASC")
    items = cur.fetchall()
    cur.execute("SELECT ean FROM movies WHERE title IS NULL")
    unsorteditems = cur.fetchall()
     
    return render_template("index.html", items=items, unsorteditems=unsorteditems)

@app.route("/search")
def search():
    search_text = request.args.get("q")
    DB = sqlite3.connect("test.db")
    DB.row_factory = sqlite3.Row
    cur = DB.cursor()
    cur.execute("SELECT ean, title, imgfile, duration FROM movies WHERE title LIKE ?", ("%" + search_text + "%",))
    items = cur.fetchall()
    return render_template("index.html", items=items)

@app.route("/product/<ean>")
def dvdpage(ean):
    DB = sqlite3.connect("test.db")
    DB.row_factory = sqlite3.Row
    cur = DB.cursor()
    cur.execute("SELECT * FROM movies WHERE ean LIKE ?", (ean,))
    res = cur.fetchone()
    return render_template("detail.html", **res)

@app.route("/errors", methods=["GET", "POST"])
def errors():
    DB = sqlite3.connect("test.db")
    DB.row_factory = sqlite3.Row
    cur = DB.cursor()
    
    #Process POST data when available
    resolved_data = []
    for oldean, newean in request.form.items():
        if newean.strip() != "":
            d = resolve_ean(newean, "images")
            resolved_data.append(d)
            cur.execute("UPDATE movies SET title=?, description=?, duration=?, imgfile=?, studio=? WHERE ean=?", (d["title"], d["description"], d["duration"], d["imgfile"], d["studio"], oldean))
            DB.commit()

    cur.execute("SELECT ean FROM movies WHERE title IS NULL")
    unsorteditems = cur.fetchall()

    return render_template("errors.html", eanlist=unsorteditems, resolved_data=resolved_data)

@app.route("/add", methods=["GET", "POST"])
def add():
    d = None
    if "ean" in request.form:
        d = resolve_ean(request.form["ean"], "images")
        print(d)

        DB = sqlite3.connect("test.db")
        DB.row_factory = sqlite3.Row
        cur = DB.cursor()
        cur.execute("INSERT INTO movies (ean, title, description, duration, imgfile, studio) VALUES (?, ?, ?, ?, ?, ?)", (d["ean"], d["title"], d["description"], d["duration"], d["imgfile"], d["studio"]))
        DB.commit()

    return render_template("add.html", added_item=d)

@app.route("/serversettings")
def server_settings():
    import qrcode
    import pprint
    qr = qrcode.QRCode(
                version=5,
                error_correction=qrcode.constants.ERROR_CORRECT_Q,
                box_size=10,
                border=4,
            )
    qr.add_data("192.168.178.22:5000;")
    qr.add_data("192.168.123123:5000")
    img = qr.make_image() 
    img.save("static/serverbarcode.png")
    return render_template("server_settings.html")

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
