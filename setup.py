import pathlib

from setuptools import setup

setup(
    name="spolstore",
    version="0.9",
    description="rdflib store using SQLite Fulltext index",
    long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/epoz/spolstore",
    author="epoz",
    author_email="ep@epoz.org",
    license="BSD-3-Clause",
    platforms=["any"],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database :: Database Engines/Servers",
    ],
    project_urls={
        "Documentation": "https://github.com/epoz/spolstore/blob/main/README.md",
        "Source": "https://github.com/epoz/spolstore",
        "Tracker": "https://github.com/epoz/spolstore/issues",
    },
    packages=["spolstore"],
    install_requires=["rdflib~=6.0", "apsw", "rich", "python-multipart", "starlette"],
    entry_points={
        "rdf.plugins.store": [
            "spol = spolstore:SpolStore",
        ]
    },
    include_package_data=True,
)
