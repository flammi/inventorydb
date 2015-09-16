import requests
import lxml.html
import os 
import shutil
import re
from ean_resolve.utils import defNone, toDBDate

SEARCH_URL = "https://www.rebuy.de/kaufen/suchen?q={}"
TYPE_TRANSLATE = {
    "DVD": "movie",
    "CD": "audiobook",
    "Hörbücher & Hörspiele": "audiobook"
}


def resolve_ean(ean):
    page = requests.get(SEARCH_URL.format(ean))
    html = lxml.html.document_fromstring(page.text)

    #Jump further
    further_url = "http://www.rebuy.de/" + html.find('.//a[@class="productConversion"]').attrib["href"]
    
    page = requests.get(further_url)
    html = lxml.html.document_fromstring(page.text)
    result = dict()
    result["title"] = html.find('.//h1/span[@class="loud"]').text_content()
    result["type"] = TYPE_TRANSLATE[html.xpath('.//p[contains(@class, "category-icon")]')[0].text_content()]
    result["imgurl"] = html.find(".//img[@id='cover']").attrib["src"] 

    attribs = dict()

    for i in html.findall(".//ul[@id='main-info-facts']/li"):
        name, sep, val = i.text_content().strip().partition(":")
        attribs[name] = val

    result["created"] = defNone(attribs.get("Erscheinungsdatum"), lambda x: toDBDate(x.strip(), "%d.%m.%Y"))
    result["author"] = None
    result["artists"] = None
    result["description"] = None
    result["duration"] = None
    
    return result

def test_rebuy():
    print(resolve_ean(4010232012210))
    print(resolve_ean(9783899641844))
    print(resolve_ean("9783898133098"))
    print(resolve_ean("9783837121834"))
    print(resolve_ean("9783867420761"))
