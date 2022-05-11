'''Utility functions used by the fetch CLI tool.'''

import datetime
import os
import re
import requests
from bs4 import BeautifulSoup

DOWNLOADS_FOLDER_NAME = "downloads"

def download_site(url):
    '''Sends an HTTP request to provided URL and saves response to file on local disk. Prints metadata.'''
    try:
        page = requests.get(url)
    except requests.exceptions.InvalidSchema:
        print(f'{bcolors.FAIL}ERROR: Connection to {url} failed. Please ensure this is a valid URL and try again.{bcolors.ENDC}')
        exit(1)
    except:
        print(f'{bcolors.FAIL}ERROR: Something went wrong downloading {url}. Please ensure you can access URL by CLI (ping, curl, etc.) and try again.{bcolors.ENDC}')
        exit(1)
        
    path = get_url_file_path(url)
    with open(path, "w") as file:
        file.write(str(page.text))
        print(f"{bcolors.OKGREEN}SUCCESS: {url} was successfully downloaded!{bcolors.ENDC}")
        print_metadata(url)
    
def folder_create():
    '''Creates destination download folder to store HTML files.'''
    try:
        print(f"{bcolors.OKBLUE}INFO: Creating '{DOWNLOADS_FOLDER_NAME}' folder in current directory...{bcolors.ENDC}")
        os.mkdir(DOWNLOADS_FOLDER_NAME)
        print(f"{bcolors.OKGREEN}SUCCESS: '{DOWNLOADS_FOLDER_NAME}' folder successfully created in current directory.{bcolors.ENDC}")
    except:
        print(f"{bcolors.WARNING}WARNING: '{DOWNLOADS_FOLDER_NAME}' folder already exists in current directory.{bcolors.ENDC}")
        
def print_metadata(url):
    '''Prints metadata about the HTML to the console.'''
    print()
    print(f'{bcolors.OKCYAN}URL Metadata for: {url}{bcolors.ENDC}')
    
    try:
        path = get_url_file_path(url)
        with open(path) as fp:
            num_links = 0
            soup = BeautifulSoup(fp, 'html.parser')
            
            # Looks for anchor tags and then further inspects for href
            anchor_tags = soup.find_all('a')
            for anchor in anchor_tags:
                if anchor.has_attr('href'): num_links += 1
                
            # Finds all images in HTML   
            images = soup.find_all('img')
            
            print(f'    {bcolors.HEADER}num_links: {num_links}{bcolors.ENDC}')
            print(f'    {bcolors.HEADER}images: {len(images)}{bcolors.ENDC}')
    except FileNotFoundError:
        print(f"{bcolors.FAIL}ERROR: Web page not found locally. Please run 'get-url' command and retry.{bcolors.ENDC}")
        exit(1)

    # Prints file fetch timestamp information
    created_time = os.path.getctime(get_url_file_path(url))
    dt_created = datetime.datetime.fromtimestamp(created_time, tz=datetime.timezone.utc)
    print(f'    {bcolors.HEADER}last_fetch: {dt_created.strftime("%a %B %d %Y %I:%M UTC")}{bcolors.ENDC}')
    print()
        
def clean_url(url):
    '''Cleans up provided URL by removing leading http:// or https://'''
    return re.sub('http[s]?://', '', url)

def get_url_file_path(url):
    '''Appends filename to downloads folder absolute path.'''
    filename = clean_url(url) + '.html'
    return os.path.join(os.getcwd(), DOWNLOADS_FOLDER_NAME, filename)

def valid_url(url):
    '''Matches passed URL string against valid URL Regular Expression looking for http(s)://xxxxxx.xxx
    Example pulled from: https://www.geeksforgeeks.org/check-if-an-url-is-valid-or-not-using-regular-expression/
    '''
    regex = "((http|https)://)(www.)?" + "[a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]" + "{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)"
    regex = re.compile(regex)
    if(re.search(regex, url)):
        return True
    else:
        print(f"{bcolors.FAIL}ERROR: {url} failed URL check. Please ensure you've input valid URL(s) including protocol (http/s).{bcolors.ENDC}")
        exit(1)

'''Colors for prettier output text to console'''
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'