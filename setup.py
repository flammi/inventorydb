import setuptools
from distutils.core import setup

setup(
        name="inventorydb",
        author="Fabian Franzen",
        author_email="flammi88@gmail.com",
        packages=["inventorydb.ean_resolve", "inventorydb.web", "inventorydb.desk"],
        package_dir = {"inventorydb": ""}
)
