import ean_resolve.thalia
import ean_resolve.buecher_de
import os.path
import re
from ean_resolve.utils import download_image

RESOLVERS = [
    ("Thalia", thalia.resolve_ean),
    ("Buecher.de", buecher_de.resolve_ean)
]

class EANNotResolved(Exception):
    pass

def resolve_ean(ean, dl_dir):
    for storename, func in RESOLVERS:
        res = func(ean)
        
        #When the resolver found something -> return result and exit
        if res:
            res["ean"] = ean
            if dl_dir:
                filename = "{title}-{ean}.jpg".format(ean=res["ean"], title=re.sub("\W","", res["title"]))  
                download_image(res["imgurl"], os.path.join(dl_dir, filename))
                res["imgfile"] = filename
            return res
    #When nothing has been found raise execption
    raise EANNotResolved()
