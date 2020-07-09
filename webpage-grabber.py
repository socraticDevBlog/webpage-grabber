import requests
import re
import sys
import logging
from datetime import datetime
import os
from tld import get_tld
    
URL_INDEX = 1
EXTRA_LABEL_INDEX = 2
MINIMUM_ARGS_COUNT = 2
LOG_FILE_NAME = 'history.log'
OUTPUT_DIRECTORY_NAME = 'output'
SPACER_CHAR = '_'


path = os.getcwd()
Format_String = "%Y-%m-%d-%H-%M-%S"
timestamp = datetime.utcnow().strftime(Format_String)
logname = os.path.join(path, LOG_FILE_NAME)

logging.basicConfig(filename=logname,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

args_count = len(sys.argv)

if args_count < MINIMUM_ARGS_COUNT:
    logging.warning('Failed: kindly provide a valid URL as 1st parameter: $python webpage-grabber.py https://mysite.cohttp://ftp.nasa.com/m')
    sys.exit('EXIT: Failed: kindly provide a valid URL as 1st parameter: $python webpage-grabber.py https://mysite.com')

url = str(sys.argv[URL_INDEX])

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

downloads_dir = os.path.join(path,OUTPUT_DIRECTORY_NAME)

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

if args_count == MINIMUM_ARGS_COUNT:
    file_name = os.path.join(downloads_dir, site_name + SPACER_CHAR + timestamp + '.html')
else:
    extra_label = str(sys.argv[EXTRA_LABEL_INDEX])
    file_name = os.path.join(downloads_dir, site_name + SPACER_CHAR + extra_label + SPACER_CHAR + timestamp + SPACER_CHAR + '.html')

try:
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(site_content.text)
        logging.info('Successfully downloaded html code from: ' + url)
        sys.exit('Successfully downloaded html code from: ' + url)
except Exception as e:
    logging.error('Error: couldnt write result to file. Error message says ->' + str(e))
    sys.exit('EXIT: failed to write result to file.  Read log file for more infos when downloading -> ' + url)