import asyncio
from ean_resolver import resolve_ean
import sqlite3

#Dir where the images of the scanned products are saved
DLDIR = "images"
DB = sqlite3.connect("test.db")

class EANRemoteScannerServer(asyncio.Protocol):
    def connection_made(self, transport):
        self.db_cursor = DB.cursor()
        self.peer = transport.get_extra_info("peername")
        self.peer = "{peer[0]}:{peer[1]}".format(peer = self.peer)
        print("New Connection from", self.peer)
        self.transport = transport
    
    def data_received(self, data):
        ean = data.strip().decode()
        if len(ean) != 13:
            print("Error, not a valid EAN!")
            return

        print("[{peer}] Received EAN={ean}".format(peer = self.peer, ean=ean))

        #Save result to sqlite database
        self.db_cursor.execute("SELECT ean, title FROM movies WHERE ean=?", (ean,))
        db_set = self.db_cursor.fetchmany()
        if len(db_set) == 0:
            print("Not in DB, resolving...")
            result = resolve_ean(ean, dl_dir=DLDIR)
            print(result)
            self.db_cursor.execute("INSERT INTO movies VALUES (?,?,?,?,?,?)", (ean ,result.title, ",".join(result.artists), result.duration, None, result.studio))
            DB.commit()
            self.transport.write(("NEW: " + result.title + "\n").encode("utf-8"))
        else:
            self.transport.write(("ART: " + db_set[0][1] + "\n").encode("utf-8"))
            print("Already in DB:", db_set[0][0], "-", db_set[0][1])

    def connection_lost(self, exc):
        print("[{peer}] Lost connection!".format(peer = self.peer))


#Prepare DB
cur = DB.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS movies (ean TEXT, title TEXT, artists TEXT, duration INT, imgfile TEXT, studio TEXT)")

loop = asyncio.get_event_loop()
coro = loop.create_server(EANRemoteScannerServer, "0.0.0.0", 5050)
server = loop.run_until_complete(coro)

print("Serving on {}".format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
