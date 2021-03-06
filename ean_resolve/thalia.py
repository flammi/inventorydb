import requests
import lxml.html
import os 
from collections import defaultdict
from ean_resolve.utils import defNone, toDBDate, interpDate
import re

SEARCH_URL = "http://www.thalia.de/shop/home/suche/?sq={ean}"

def resolve_ean(ean):
    page = requests.get(SEARCH_URL.format(ean=ean))
    
    #Check if something was found
    if "Ihre Suche ergab leider keine Treffer" in page.text:
        return None

    html = lxml.html.document_fromstring(page.text)
    result = defaultdict()

    transform = list()

    #Check media type
    result["type"] = html.find('.//span[@class="noCategory"]').text_content().strip()

    resolve_author = lambda: defNone(html.find('.//span[@class="oAuthorLinked"]'), lambda x: x.text_content()) 
    if result["type"].startswith("Buch"):
        result["type"] = "book"
        result["author"] = resolve_author()
        result["artists"] = None
    elif result["type"] == "Hörbuch":
        result["type"] = "audiobook"
        result["author"] = resolve_author()
        result["artists"] = None
    else:
        result["type"] = "movie"
        result["artists"] = [elm.text for elm in html.findall('.//span[@class="oAuthorLinked"]/a')]
        result["author"] = None

    #Extract simple attributes from the head of the page
    result["title"] = html.find('.//span[@class="oProductTitle"]').text.strip()
    result["imgurl"] = html.find('.//img[@id="elevateZoom"]').attrib["src"]

    result["description"] = defNone(html.find('.//dd[@class="cTypeBeschreibung"]'), lambda x: x.text_content().strip())

    #Extract attributes of the dd/dt Table next to the article picture
    attr_container = html.find('.//dl[@class="dlCols30_70"]')

    attr_list = dict()
    for elm in attr_container.getchildren():
        if elm.tag == "dt":
            curName = elm.text.strip()
        if elm.tag == "dd":
            attr_list[curName] = elm.text_content().strip()

    result["duration"] = defNone(attr_list.get("Spieldauer"), lambda x:int(x.replace("Minuten", "")))

    result["studio"] = attr_list.get("Studio")
    result["genre"] = attr_list.get("Genre") 
    import locale
    oldlocale = locale.getlocale(locale.LC_TIME)
    locale.setlocale(locale.LC_TIME, "de_DE.utf8")
    result["created"] = defNone(attr_list.get("Erscheinungsdatum"), lambda x: interpDate(x))
    locale.setlocale(locale.LC_TIME, oldlocale)

    return result 

def test_poi3():
    d = resolve_ean("5051890287687")
    assert d["title"] == "Person of Interest - Staffel 3"
    assert d["created"] == "2014-11-06"
    assert d["type"] == "movie"
    assert d["studio"] == "Warner Home Video"

def test_medicus():
    d = resolve_ean("9783837121834")
    assert d["title"] == "Der Medicus"
    assert d["created"] == "2013-10-18"
    assert d["type"] == "audiobook"
    assert d["studio"] == None 
    assert d["author"] == "Noah Gordon"

def test_sherlockholmes():
    d = resolve_ean("9783898133098")
    assert d["title"] == "Sherlock Holmes und Dr. Watson. Die größten Fälle. 5 CDs"
    assert d["created"] == "2004-05-03"
    assert d["type"] == "audiobook"
    assert d["studio"] == None 
    assert d["author"] == "Arthur Conan Doyle"

def test_jkrowling():
    d = resolve_ean("9783551588883")
    assert d["title"] == "Ein plötzlicher Todesfall"
    assert d["created"] == "2012-09-27"
    assert d["type"] == "book"
    assert d["studio"] == None 
    assert d["author"] == "Joanne K. Rowling"

def test_various():
    print(resolve_ean("9783867420761"))
    print(resolve_ean("9783426503744"))
