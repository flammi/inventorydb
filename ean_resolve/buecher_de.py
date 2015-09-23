import requests
import lxml.html
import os 
import shutil
import re
from ean_resolve.utils import defNone, toDBDate, interpDate

SEARCH_URL = "http://www.buecher.de/go/search_search/quick_search/receiver_object/shop_search_quicksearch/"

def resolve_ean(ean):
    page = requests.post(SEARCH_URL, data={"form[q]": ean})

    #Check if something was found
    if "keine Artikel gefunden" in page.text:
        return None

    html = lxml.html.document_fromstring(page.text)
    result = dict()

    result["type"] = html.find('.//li[@class="variant"]').text_content().strip()
    if result["type"] == "Audio CD":
        result["type"] = "audiobook"
        result["author"] = html.find('.//a[@class="author"]').text_content().strip()
        result["artists"] = None
    elif result["type"] == "Gebundenes Buch":
        result["type"] = "book"
        result["author"] = html.find('.//a[@class="author"]').text_content().strip()
        result["artists"] = None
    else:
        result["artists"] = result["author"] = None
        result["type"] = "movie"


    result["title"] = html.find('.//h1[@class="headline"]').text
    attr_field = html.find('.//ul[@class="plain"]')
    attrs = dict()
    for li in attr_field.findall(".//li"):
        data = li.text_content()
        if data:
            title, sep, val = data.partition(":") 
            attrs[title] = val.strip()
    #Extract description
    description_element = html.find('.//div[@class="product-description"]/div[2]/div[1]')

    #Convert brs to nl
    if description_element is not None:
        for br in description_element.xpath(".//br"):
            br.tail = "\n" + br.tail if br.tail else "\n"
        description = description_element.text_content()

        #Strip trailing crap
        result["description"] = description[:description.find("Bonusmaterial")]
    else:
        #Ignore this hit if there is no description
        return None

    try:
        result["duration"] = int(re.search("Gesamtlaufzeit: (\d+) Min.", page.text).group(1))
    except:
        result["duration"] = None

    result["created"] = defNone(attrs.get("Erscheinungstermin"), lambda x: interpDate(x)) 
    result["studio"] = attrs.get("Hersteller")

    result["imgurl"] = html.find('.//img[@class="cover"]').attrib["src"]

    return result 

def test_poi3():
    d = resolve_ean("5051890287687")
    assert d["title"] == "Person of Interest - Die komplette dritte Staffel (6 Discs)"
    assert d["created"] == "2014-11-06"
    assert d["type"] == "movie"
    assert d["studio"] == "Warner Home Video"

def test_medicus():
    d = resolve_ean("9783837121834")
    assert d["title"] == "Der Medicus / Der Medicus Bd.1 (Audio-CD)"
    assert d["created"] == None 
    assert d["type"] == "audiobook"
    assert d["studio"] == None 
    assert d["author"] == "Noah Gordon"

def test_sherlockholmes():
    d = resolve_ean("9783898133098")
    assert d["title"] == "Sherlock Holmes & Dr. Watson, Die größten Fälle, 5 Audio-CDs"
    assert d["created"] == None
    assert d["type"] == "audiobook"
    assert d["studio"] == None 
    assert d["author"] == "Arthur C. Doyle"

def test_jkrowling():
    d = resolve_ean("9783551588883")
    assert d["title"] == "Ein plötzlicher Todesfall"
    assert d["created"] == None
    assert d["type"] == "book"
    assert d["studio"] == None 
    assert d["author"] == "Joanne K. Rowling"

