import shutil
import requests
import time
import re
from functools import wraps

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

def germanized(func):
    @wraps(func)
    def with_german_locale(*args, **kwargs):
        import locale
        oldlocale = locale.getlocale(locale.LC_TIME)
        locale.setlocale(locale.LC_TIME, "de_DE.utf8")
        res = func(*args, **kwargs)
        locale.setlocale(locale.LC_TIME, oldlocale)
        return res
    return with_german_locale

@germanized
def interpDate(date):
    date_striped = date.strip()
    dateConvert = [
        ("\d+.\d+.\d+", lambda x: toDBDate(x, "%d.%m.%Y")),
        ("\w+ \d\d\d\d", lambda x: toDBDate(x, "%B %Y")),
        ("\d+\. \w+ \d\d\d\d", lambda x: toDBDate(x, "%d. %B %Y"))
        ]
    for pattern, convertFunc in dateConvert:
        if re.match(pattern, date_striped):
            return convertFunc(date_striped)
    
