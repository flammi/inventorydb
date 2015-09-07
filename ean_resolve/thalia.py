import requests
import lxml.html
import os 

SEARCH_URL = "http://www.thalia.de/shop/home/suche/?sq={ean}"

def resolve_ean(ean):
    page = requests.get(SEARCH_URL.format(ean=ean))
    
    #Check if something was found
    if "Ihre Suche ergab leider keine Treffer" in page.text:
        return None

    html = lxml.html.document_fromstring(page.text)
    result = dict()
    
    #Check media type
    result["type"] = html.find('.//span[@class="noCategory"]').text_content().strip()

    #Extract simple attributes from the head of the page
    result["title"] = html.find('.//span[@class="oProductTitle"]').text
    result["imgurl"] = html.find('.//img[@id="elevateZoom"]').attrib["src"]
    result["artists"] = [elm.text for elm in html.findall('.//span[@class="oAuthorLinked"]/a')]
    try:
        result["description"] = html.find('.//dd[@class="cTypeBeschreibung"]').text.strip()
    except Exception as e:
        print("Missing description at EAN", ean)
        result["description"] = None

    #Extract attributes of the dd/dt Table next to the article picture
    attr_container = html.find('.//dl[@class="dlCols30_70"]')

    attr_list = dict()
    for elm in attr_container.getchildren():
        if elm.tag == "dt":
            curName = elm.text.strip()
        if elm.tag == "dd":
            attr_list[curName] = elm.text_content().strip()

    result["duration"] = int(attr_list.get("Spieldauer").replace("Minuten", ""))
    result["studio"] = attr_list.get("Studio")
    result["genre"] = attr_list.get("Genre") 
    result["created"] = attr_list.get("Erscheinungsdatum") 

    return result 

if __name__ == "__main__":
    print(resolve_ean("5051890287687"))
    print(resolve_ean("9783837121834"))
