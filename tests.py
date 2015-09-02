from ean_resolve import resolve_ean
import pathlib

EANS = [
    4010232055620,
    4010232046369,
    5050582871753,
    5051890139610,
    4045167004429
]

if __name__ == "__main__":
#    try:
        dl_dir = "images"
        dl_dir_path = pathlib.Path(dl_dir)
        if not dl_dir_path.exists():
            dl_dir_path.mkdir()
        for ean in EANS:
            print(resolve_ean(ean, dl_dir=dl_dir))

#    except:
#        import pdb;
#        pdb.post_mortem()
