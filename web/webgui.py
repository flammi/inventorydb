#!/usr/bin/python3
from flask import Flask, render_template, request, g, jsonify
import datetime
from flask.json import jsonify
app = Flask(__name__)
import sqlite3

from ean_resolve import resolve_ean

def get_db():
    db = getattr(g, 'database', None)
    if db is None:
        db = g.database = sqlite3.connect("test.db")
        db.row_factory = sqlite3.Row
    return db

def query_db(statement, args=None):
    cur = get_db().cursor()
    if args is None:
        cur.execute(statement)
    else:
        cur.execute(statement, args)
    return cur.fetchall()

@app.teardown_appcontext
def close_db_connection(exception):
    db = getattr(g, 'database', None)
    if db is not None:
        db.close()

def save_choice(args_dict, key, choices, default=None):
    if default is None:
        default = choices[0]
    result = args_dict.get(key, default)
    if result not in choices:
        result = default
    return result

def ean_add_to_db(ean):
    d = resolve_ean(ean, "images")
    d["added_date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print(d)

    cur = get_db().cursor()
    cur.execute("INSERT INTO inventory (ean, category, title, description, duration, imgfile, author, artists, created, added) VALUES (:ean, :type, :title, :description, :duration, :imgfile, :author, :artists, :created, :added_date)", d)
    get_db().commit()

    return d

@app.route("/")
def main():
    sortorder = save_choice(request.args, "order", ["title", "ean", "duration", "created"])
    direction = save_choice(request.args, "dir", ["asc", "desc"])
    
    items = query_db('SELECT * FROM inventory WHERE category = "movie" and title IS NOT NULL ORDER BY {} {}'.format(sortorder, direction))

    return render_template("index.html", items=items)

@app.route("/audiobooks")
def audiobooks():
    sortorder = save_choice(request.args, "order", ["title", "ean", "duration", "created"])
    direction = save_choice(request.args, "dir", ["asc", "desc"])
    
    items = query_db('SELECT * FROM inventory WHERE category = "audiobook" and title IS NOT NULL ORDER BY {} {}'.format(sortorder, direction))

    return render_template("index.html", items=items)

@app.route("/books")
def books():
    sortorder = save_choice(request.args, "order", ["title", "ean", "duration", "created"])
    direction = save_choice(request.args, "dir", ["asc", "desc"])
    
    items = query_db('SELECT * FROM inventory WHERE category = "book" and title IS NOT NULL ORDER BY {} {}'.format(sortorder, direction))
    return render_template("index.html", items=items)

@app.route("/search")
def search():
    search_text = request.args.get("q")
    cur = get_db().cursor()
    cur.execute("SELECT ean, title, imgfile, duration FROM movies WHERE and title LIKE ?", ("%" + search_text + "%",))
    items = cur.fetchall()
    return render_template("index.html", items=items)

@app.route("/product/<ean>")
def dvdpage(ean):
    cur = get_db().cursor()
    cur.execute("SELECT * FROM inventory WHERE ean LIKE ?", (ean,))
    res = cur.fetchone()
    return render_template("detail.html", **res)

@app.route("/errors", methods=["GET", "POST"])
def errors():
    cur = get_db().cursor()
    
    #Process POST data when available
    resolved_data = []
    for oldean, newean in request.form.items():
        if newean.strip() != "":
            d = resolve_ean(newean, "images")
            resolved_data.append(d)
            cur.execute("UPDATE movies SET title=:title, description=:description, duration=:duration, imgfile=:imgfile, studio=:studio WHERE ean=:ean", d)
            get_db().commit()

    cur.execute("SELECT ean FROM movies WHERE title IS NULL")
    unsorteditems = cur.fetchall()

    return render_template("errors.html", eanlist=unsorteditems, resolved_data=resolved_data)

@app.route("/add", methods=["GET", "POST"])
def add():
    d = None
    if "ean" in request.form:
        d = ean_add_to_db(request.form["ean"])

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


import traceback

#REST-API for Smartphone Scanner
@app.route("/scannerapi", methods=["POST"])
def push_scan_result():
    ean = request.form["ean"]
    try:
        res = query_db("SELECT * FROM inventory WHERE ean=?",[ean])
        if len(res) == 0:
            d = ean_add_to_db(ean)
            d["newentry"] = True
        else:
            d = dict(res[0])
            d["newentry"] = False 
        return jsonify(d)
    except:
        cur = get_db().cursor()
        cur.execute("INSERT INTO errors VALUES (:ean, :stacktrace)", {"ean":ean, "stacktrace": traceback.format_exc()})
        get_db().commit()
        return jsonify({"error": True})

@app.route("/scannerapi", methods=["GET"])
def push_scan_result_get():
    d = query_db("SELECT * FROM movies")
    return jsonify(d[0])

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
