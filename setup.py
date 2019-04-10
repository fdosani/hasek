import os
from setuptools import setup

CURR_DIR = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(CURR_DIR, "README.md"), encoding="utf-8") as file_open:
    LONG_DESCRIPTION = file_open.read()

with open(os.path.join(CURR_DIR, "requirements.txt"), encoding="utf-8") as file_open:
    INSTALL_REQUIRES = file_open.read().split("\n")

exec(open("hasek/_version.py").read())

setup(
    name="hasek",
    version=__version__,
    description="Password Management for Humans",
    long_description=LONG_DESCRIPTION,
    url="https://github.com/fdosani/hasek",
    author="Faisal Dosani",
    author_email="faisal.dosani@gmail.com",
    license="MIT",
    packages=["hasek"],
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': [
            'hasek = hasek.__main__:main'
        ]
    },
    zip_safe=False,
)