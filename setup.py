from setuptools import setup, find_packages
import json


with open("metadata.json", encoding="utf-8") as fp:
    metadata = json.load(fp)


setup(
    name='lexibank_chindialectsurvey',
    version="1.0",
    description=metadata['title'],
    license=metadata.get('license', ''),
    url=metadata.get('url', ''),
    py_modules=['lexibank_chindialectsurvey'],
    include_package_data=True,
    packages=find_packages(where="."),
    zip_safe=False,
    entry_points={
        'lexibank.dataset': [
            'chindialectsurvey=lexibank_chindialectsurvey:Dataset',
        ],
        'cldfbench.commands': [
            'chindialectsurvey=commands',
        ]
    },
    install_requires=[
        'pylexibank>=3.0',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
