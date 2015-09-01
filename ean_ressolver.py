import requests
import os.path
import lxml.html
import shutil
import pathlib
from collections import namedtuple

SEARCH_URL = "http://www.thalia.de/shop/home/suche/?sq={ean}"

DVDMovie = namedtuple("DVDMovie", ["title", "img_url", "artists", "duration", "studio", "genre", "created", "description"])

def resolve_ean(ean, dl_dir=None):
    page = requests.get(SEARCH_URL.format(ean=ean))
    html = lxml.html.document_fromstring(page.text)

    #Extract simple attributes from the head of the page
    dvd_title = html.find('.//span[@class="oProductTitle"]').text
    img_url = html.find('.//img[@id="elevateZoom"]').attrib["src"]
    artists = [elm.text for elm in html.findall('.//span[@class="oAuthorLinked"]/a')]
    try:
        description = html.find('.//dd[@class="cTypeBeschreibung"]').text.strip()
    except Exception as e:
        print("Missing description at EAN", ean)
        description = None

    #Extract attributes of the dd/dt Table next to the article picture
    attr_dd = html.findall('.//dl[@class="dlCols30_70"]/dd')
    attr_dt = html.findall('.//dl[@class="dlCols30_70"]/dt')

    attr_elm_list = zip(attr_dt, attr_dd)
    attr_list = dict()
    for attr_name, attr_val in attr_elm_list:
        attr_list[attr_name.text.strip()] = attr_val.text.strip()

    duration = int(attr_list.get("Spieldauer").replace("Minuten", ""))
    studio = attr_list.get("Studio")
    genre = attr_list.get("Genre") 
    created = attr_list.get("Erscheinungsdatum") 

    #Download image to dl_dir if requested
    if dl_dir:
        download_image(img_url, os.path.join(dl_dir, "{dvd_title} - {ean}.jpg".format(ean=ean, dvd_title=dvd_title)))

    return DVDMovie(dvd_title, img_url, artists, duration, studio, genre, created, description)

def download_image(url, filename):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(filename, "wb") as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f) 
    

if __name__ == "__main__":
#    try:
        dl_dir = "images"
        dl_dir_path = pathlib.Path(dl_dir)
        if not dl_dir_path.exists():
            dl_dir_path.mkdir()
        res = resolve_ean(4010232055620, dl_dir=dl_dir)
        print(res)
        print(resolve_ean(4010232046369, dl_dir=dl_dir))
        print(resolve_ean(5050582871753, dl_dir=dl_dir))
        print(resolve_ean(5051890139610, dl_dir=dl_dir))
#    except:
#        import pdb;
#        pdb.post_mortem()

