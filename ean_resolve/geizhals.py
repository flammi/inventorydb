import requests
import lxml.html
import os 
import re
from collections import defaultdict
from ean_resolve.utils import defNone 

SEARCH_URL = "http://geizhals.de/?fs={}"

def resolve_ean(ean):
    page = requests.get(SEARCH_URL.format(ean))
    html = lxml.html.document_fromstring(page.text)
    
    result = dict()
    title_elm = html.find(".//span[@itemprop='name']")

    #When the title is not found on the page, the product seems to be in the unsorted section of geizhals...
    if title_elm is None:
        return None

    result["title"] = title_elm.text_content()
    result["genre"] = html.find(".//li[@class='ghnavhi']").text_content()
    description = html.find(".//div[@id='gh_proddesc']").text_content()
    result["firstrelease"] = defNone(re.search("Ersterscheinung: (\d+)", description), lambda x: x.group(1))

    for i in html.findall(".//a[@class='revlink']"):
        if "imdb" in i.attrib["href"]:
            result["imdb_link"] = i.attrib["href"]
            break;

    return result

if __name__ == "__main__":
    print(resolve_ean(5051890019288))
    print(resolve_ean("4045167004429"))
    print(resolve_ean("4010232028969"))
    print(resolve_ean("5051890287687"))
