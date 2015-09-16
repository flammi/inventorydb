import shutil
import requests
import time

def download_image(url, filename):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(filename, "wb") as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f) 

def defNone(call_res, ppfunc):
    if call_res is not None:
        return ppfunc(call_res)
    else:
        return None

def toDBDate(date, format):
    return time.strftime("%Y-%m-%d", time.strptime(date, format))
