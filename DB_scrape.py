import sys
import requests
import browser_cookie3
import bs4
import pandas as pd
import io
import os
import zipfile
from progressbar import progressbar
import warnings
warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)

# Check 'writedisk' option
# If not present, do everything in memory
try:
    writedisk = sys.argv[2]
except IndexError:
    writedisk = 'no'

# Determine boolean
if 'writedisk' in writedisk:
    writedisk = True
else:
    writedisk = False

# Read, filter, and return dataframe
def read_filter(file, indices, writedisk = False):
    df = pd.read_csv(file, sep = '\t', header = None, usecols = indices)
    df = df[df[44].astype(str).apply(lambda x: x.isnumeric())]
    df = df[df[44].astype(str).astype(int).between(2000, 4000)]
    if writedisk:
        df['date'] = file.split('.')[3]
    else:
        df['date'] = file.name.split('.')[3]
    return df

# Function to download and write file directly to current dir
def download(url, filename):
    if os.path.isfile(filename):
        print(filename, 'exists')
        return

    with open(filename, 'wb') as f:
        response = requests.get(url + filename, stream=True, cookies = cj)
        total = response.headers.get('content-length')

        if total is None:
            f.write(response.content)
        else:
            downloaded = 0
            total = int(total)
            for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                downloaded += len(data)
                f.write(data)
                done = int(50*downloaded/total)
                sys.stdout.write('\r[{}{}]'.format('#' * done, '.' * (50-done))+filename)
                sys.stdout.flush()
    sys.stdout.write('\n')

# Create index list for relevant columns
indices = [1, 2, 3, 6, 14, 20] + list(range(45, 62)) + [74, 76, 84, 90, 91, 116, 117, 130, 131]
indices = [x - 1 for x in indices]  # because python is 0-indexed

# Request list index
# Index URL is 'https://dss2.princeton.edu/dandb/dandbarchives/LINK/<subdir>/'
base_url = 'https://vpn.princeton.edu/https-443/'
url = base_url + sys.argv[1].replace('https://', '')
# url = 'https://vpn.princeton.edu/https-443/dss2.princeton.edu/dandb/dandbarchives/LINK/EU/'
cj = browser_cookie3.firefox()
r = requests.get(url, cookies = cj)
soup = bs4.BeautifulSoup(r.text, 'html.parser')

# Download, filter and join files in memory
if not writedisk:
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

# Download files, write them to disk, and join them separately
if writedisk:
    # Download
    if len(sys.argv) == 3 or sys.argv[3] == 'download':
        print('downloading files...')
        for l in soup.find_all(lambda tag: tag.name=='a' and tag['href'].endswith('.zip')):
            filename = l['href']
            if os.path.isfile(filename):
                print(f"File {filename} exists")
            else:
                download(url, filename)

    # Filter
    if len(sys.argv) == 3 or sys.argv[3] == 'filter':
        print('filtering data...')
        # dfs = []
        zip_files = sorted([f for f in os.listdir('.') if f.endswith('.zip')])
        csv_files = sorted([f for f in os.listdir('.') if f.endswith('.csv')])
        zip_files = sorted(list(set([os.path.splitext(x)[0] for x in zip_files]) - set([os.path.splitext(x)[0] for x in csv_files])))
        for file in progressbar(zip_files, redirect_stdout=True):
            print(file + '.csv')
            df = read_filter(file + '.zip', indices, writedisk=True)
            # dfs.append(df)
            df.to_csv(file + '.csv', index=False)

    # Join and write (in memory)
    # if len(sys.argv) == 3 or sys.argv[3] == 'join':
    #     print('joining files...')
    #     dfs = pd.concat(dfs)
    #     fileout = url.split('/')[-2] + '.csv'
    #     dfs.to_csv(fileout)

    # Join and write (in disk)
    if len(sys.argv) == 3 or sys.argv[3] == 'join':
        print('joining files...')
        dfs = []
        csv_files = sorted([f for f in os.listdir('.') if f.endswith('.csv')])
        for file in progressbar(csv_files, redirect_stdout=True):
            print(file)
            dfs.append(pd.read_csv(file))

        full_df = pd.concat(dfs)
        full_df.to_csv(file + '.csv', index=False)
