import multiprocessing
from desk.qt import start_desk
from web.webgui import app

p = multiprocessing.Process(target=app.run)
p.start()
start_desk()
p.terminate()
p.join()
