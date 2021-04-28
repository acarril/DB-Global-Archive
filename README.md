# Dun & Bradstreet Global Archive scraper

This script is intended to download, filter and concatenate data files from the [Dun & Bradstreet](https://www.dnb.com/) "Global Archive" (see the [user guide](/D&BHistoricalGlobal-UserGuide.pdf)).
The data is stored in Princeton servers, and this script will only work if you are connected to the Princeton network (either directly or through a VPN; see below).

# Install & run

1. Clone this repository into your local machine and change directory into it ([detailed guide](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository)).
The easiest way is to type the following in your terminal:
```sh
git clone https://github.com/acarril/DB-Global-Archive.git
cd DB-Global-Archive
```
2. Run `DB_scrape.py` giving the file index URL as its argument. *Make sure to include the final slash*. For example, to download the data corresponding to Africa, type
```sh
python3 DB_scrape.py 'https://dss2.princeton.edu/dandb/dandbarchives/LINK/AF/'
```

