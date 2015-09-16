import requests
import lxml.html
import os 
import shutil
import re

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
        result["artists"] = result["author"] = html.find('.//a[@class="author"]').text_content().strip()
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

    result["created"] = attrs.get("Erscheinungstermin")
    result["studio"] = attrs.get("Hersteller")

    result["imgurl"] = html.find('.//img[@class="cover"]').attrib["src"]

    return result 


if __name__ == "__main__":
    print(resolve_ean("4010232012210"))
    print(resolve_ean("9783899641844"))
#print(resolve_ean("4045167004429"))
#print(resolve_ean("4010232028969"))

