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
    for br in description_element.xpath(".//br"):
        br.tail = "\n" + br.tail if br.tail else "\n"
    description = description_element.text_content()

    #Strip trailing crap
    result["description"] = description[:description.find("Bonusmaterial")]

    result["duration"] = int(re.search("Gesamtlaufzeit: (\d+) Min.", page.text).group(1))
    result["created"] = attrs["Erscheinungstermin"]
    result["studio"] = attrs["Hersteller"]

    result["imgurl"] = html.find('.//img[@class="cover"]').attrib["src"]

    return result 


if __name__ == "__main__":
    print(resolve_ean("4010232012210"))
#print(resolve_ean("4045167004429"))
#print(resolve_ean("4010232028969"))

