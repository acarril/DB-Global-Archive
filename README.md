# Dun & Bradstreet Global Archive scraper

This script is intended to download, filter and concatenate data files from the [Dun & Bradstreet](https://www.dnb.com/) "Global Archive" (see the [user guide](/D&BHistoricalGlobal-UserGuide.pdf)).
The data is stored in Princeton servers, and this script will only work if you are connected to the Princeton network (either directly or through a VPN; see below).

# Requirements

This script has been tested on Windows 10, macOS 10.15, Manjaro Linux and Raspberry Pi OS.
Before running, make sure your machine satisfies the following requirements:
1. [Firefox](https://www.mozilla.org/firefox/) (note: it should work on Chrome, but it has not been tested)
2. Python 3
3. Python 3 modules: [requests](https://pypi.org/project/requests/), [browser_cookie3](https://pypi.org/project/browser-cookie3/), [beautifulsoup4](https://pypi.org/project/beautifulsoup4/), [pandas](https://pypi.org/project/pandas/), [progressbar2](https://pypi.org/project/progressbar2/)

## VPN access and browser cookies

This script relies on the access cookies stored in the browser (i.e. Firefox). In order for it to run correctly,
1. Browse to https://vpn.princeton.edu/https-443/dss2.princeton.edu/dandb/dandbarchives/LINK/ in Firefox.
2. If you get a Central Authentication Service (CAS) login page, use your Princeton credentials to log in. If you can access the link (i.e. you see the file directory), you are ready to run the script.
3. In the following page you should get a [Duo Prompt](https://guide.duo.com/prompt). Login via your preferred method, but **make sure you check "Remember me for 90 days"**.
4. If you see the file directory, you are done.
5. Double check the browser stored your credentials by restarting it and visiting the link again. If you can access the link directly, you are ready to run the script.

# Installation

1. Clone this repository into your local machine and change directory into it ([detailed guide](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository)).
The easiest way is to type the following two commands in your terminal:
```sh
git clone https://github.com/acarril/DB-Global-Archive.git
cd DB-Global-Archive
```
2. Run `DB_scrape.py` giving the file index URL as its argument. *Make sure to include the final slash*. For example, to download the data corresponding to Africa, type
```sh
python3 DB_scrape.py 'https://dss2.princeton.edu/dandb/dandbarchives/LINK/AF/'
```
3. The script will output its progress. Once it has finished, it will write a `csv` file in the directory (e.g. `AF.csv`).

# Usage

```sh
python3 DB_scrape.py "<url>" [writedisk] [suboperation]
```

## In memory

You can carry out all the operations in memory if running ```python3 DB_scrape.py "<url>"```. This will fetch all the links from the URL, read the data, filter it, and append it to a final dataset that will only be written in disk in the final step. This is best when there is little available disk space, and it is also faster. However, it can be memory intensive, and any error during the operation will result in loss of all progress.

## In disk

Alternatively, the script can download and write the zip files into the disk, as well as expanding the zip files and writing the corresponding CSV files into the disk, by running ```python3 DB_scrape.py "<url>" writedisk```.
This is less memory intensive and is more robust to errors (as progress is literally saved into the disk), but utilizes more disk space.

This method can be further customized by passing an additional argument with a sub-operation. These can be one of the following:
- ```download```, which only downloads the ZIP files from the specified URL
- ```filter```, which takes ZIP files already downloaded in the directory and filters the corresponding CSV files, writing them into the disk
- ```join```, which takes CSV files in the current directory and joins them into one.

