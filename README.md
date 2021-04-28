# Dun & Bradstreet Global Archive scraper

This script is intended to download, filter and concatenate data files from the [Dun & Bradstreet](https://www.dnb.com/) "Global Archive" (see the [user guide](/D&BHistoricalGlobal-UserGuide.pdf)).
The data is stored in Princeton servers, and this script will only work if you are connected to the Princeton network (either directly or through a VPN; see below).

# Requirements

This script has been tested on Windows 10, macOS 10.15, Manjaro Linux and Raspberry Pi OS.
Before running, make sure your machine satisfies the following requirements:
1. Firefox (note: it should work on Chrome, but it has not been tested)
2. Python 3
3. Python 3 modules: [browser_cookie3](https://pypi.org/project/browser-cookie3/), [beautifulsoup4](https://pypi.org/project/beautifulsoup4/), [pandas](https://pypi.org/project/pandas/), [progressbar2](https://pypi.org/project/progressbar2/)

## VPN access and browser cookies

This script relies on the access cookies stored in the browser (i.e. Firefox). In order for it to run correctly,
1. Browse to https://vpn.princeton.edu/https-443/dss2.princeton.edu/dandb/dandbarchives/LINK/ in Firefox.
2. If you get a Central Authentication Service (CAS) login page, use your Princeton credentials to log in. If you can access the link (i.e. you see the file directory), you are ready to run the script.
3. In the following page you should get a [Duo Prompt](https://guide.duo.com/prompt). Login via your preferred method, but **make sure you check "Remember me for 90 days"**.
4. If you see the file directory, you are done.
5. Double check the browser stored your credentials by restarting it and visiting the link again. If you can access the link directly, you are ready to run the script.

# Install & run

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

