import multiprocessing
from desk.qt import start_desk
import web.webgui

p = multiprocessing.Process(target=web.webgui.start_server)
p.start()
start_desk()
p.terminate()
p.join()
