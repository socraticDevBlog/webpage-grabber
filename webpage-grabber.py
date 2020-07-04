import requests
import re
import sys
import logging
from datetime import datetime
import os
from tld import get_tld
    

path = os.getcwd()
Format_String = "%d-%b-%Y-%H-%M-%S-%f"
timestamp = datetime.utcnow().strftime(Format_String)
logname = os.path.join(path, 'history.log')

logging.basicConfig(filename=logname,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

if len(sys.argv) < 2:
    logging.warning('expecting url as 1st parameter')
    sys.exit('EXIT: no url provided')

url = str(sys.argv[1])

logging.info('Downloading html code from: ' + url)

regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

is_valid_url = re.match(regex, url)

if not is_valid_url:
    logging.warning('invalid url provided')
    sys.exit('EXIT: invalid url provided')

downloads_dir = os.path.join(path,'downloads')

res = get_tld(url, as_object=True)
site_name = res.fld
site_content = requests.get(url)

file_name = os.path.join(downloads_dir, site_name + timestamp + '.html')

with open(file_name,'w', encoding='utf-8') as file:
    file.write(site_content.text)

logging.info('Success html code from: ' + url)