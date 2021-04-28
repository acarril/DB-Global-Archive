import sys
import requests
import browser_cookie3
import bs4
import pandas as pd
import io
import zipfile
from progressbar import progressbar
import warnings
warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)

# Read, filter, and return dataframe
def read_filter(file, indices):
    df = pd.read_csv(file, sep = '\t', header = None, usecols = indices)
    df = df[df[44].astype(str).apply(lambda x: x.isnumeric())]
    df = df[df[44].astype(str).astype(int).between(2000, 4000)]
    df['date'] = file.name.split('.')[3]
    return df

# Create index list for relevant columns
indices = [1, 2, 3, 6, 14, 20] + list(range(45, 62)) + [74, 76, 84, 90, 91, 116, 117, 130, 131]
indices = [x - 1 for x in indices]  # because python is 0-indexed

# Request list index
# Index URL is 'https://dss2.princeton.edu/dandb/dandbarchives/LINK/<subdir>/'
base_url = 'https://vpn.princeton.edu/https-443/'
url = base_url + sys.argv[1].replace('https://', '')
cj = browser_cookie3.firefox()
r = requests.get(url, cookies = cj)
soup = bs4.BeautifulSoup(r.text, 'html.parser')

# Loop
dfs = []
for l in progressbar(soup.find_all(lambda tag: tag.name=='a' and tag['href'].endswith('.zip'))):
    filename = l['href']
    r_file = requests.get(url + filename, cookies = cj)
    the_zipfile = zipfile.ZipFile(io.BytesIO(r_file.content))
    # open(filename, 'wb').write(r_file.content)    # write zipfile to disk; unnecessary
    df = read_filter(the_zipfile.open(the_zipfile.namelist()[0]), indices)
    dfs.append(df)

dfs = pd.concat(dfs)
fileout = url.split('/')[-2] + '.csv'
dfs.to_csv(fileout)
