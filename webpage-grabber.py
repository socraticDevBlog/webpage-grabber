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
    logging.warning('Failed: kindly provide a valid URL as 1st parameter: $python webpage-grabber.py https://mysite.cohttp://ftp.nasa.com/m')
    sys.exit('EXIT: Failed: kindly provide a valid URL as 1st parameter: $python webpage-grabber.py https://mysite.com')

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
    logging.warning('Failed: invalid url provided (full format required ex.: https//mysite.com): ' + url)
    sys.exit('EXIT: Failed: invalid url provided (full format required ex.: https//mysite.com): ' + url)

downloads_dir = os.path.join(path,'downloads')

res = get_tld(url, as_object=True)
site_name = res.fld

try:
    site_content = requests.get(url)
except Exception as e:
    logging.error('Error: http request (Get) failed. Error message says ->' + str(e))
    sys.exit('EXIT: http request (Get) failed.  Read log file for more infos when downloading -> ' + url) 

if site_content.status_code == 404:
    logging.warning('Failed: 404 not found ' + url)
    sys.exit('EXIT: 404 not found: ' + url)

if site_content.status_code == 500:
    logging.warning('Failed: 500 - Forbidden or server failure ' + url)
    sys.exit('EXIT: 500 - Forbidden or server failure: ' + url)

file_name = os.path.join(downloads_dir, site_name + timestamp + '.html')

try:
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(site_content.text)
        logging.info('Successfully downloaded html code from: ' + url)
        sys.exit('Successfully downloaded html code from: ' + url)
except Exception as e:
    logging.error('Error: couldnt write result to file. Error message says ->' + str(e))
    sys.exit('EXIT: failed to write result to file.  Read log file for more infos when downloading -> ' + url)