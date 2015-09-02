import requests
import os.path
import lxml.html
import shutil
import pathlib
from collections import namedtuple

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

