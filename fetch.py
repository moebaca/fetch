#!/usr/bin/env python
"""A simple command line tool for downloading HTML of web pages locally on disk."""

import lib.fetch_utils as fetch_utils
import fire

def get_url(urls: str):
    '''
    Download one or many HTML web pages to local disk for user access. 
    
    Pass one or many comma-separated URLs for download. 
    Pass only valid URL patterns or you may experience unexpected behavior.
    
    Example Usage:
        Single URL:
        ./fetch.py get-url --urls="https://hopkinsresu.me"
        
        Multiple URLs:
        ./fetch.py get-url --urls="https://hopkinsresu.me","https://autify.com"
   '''
    fetch_utils.folder_create()
    urls = urls.split(",")
    for url in urls:
        if url: fetch_utils.download_site(url)
        
def describe_url_metadata(urls: str):
    '''
    View the metadata for one or many HTML web pages previously saved to local disk without redownloading them over the internet. 
    
    Pass one or many comma-separated URLs for metadata viewing. 
    Pass only valid URL patterns or you may experience unexpected behavior.
    
    Example Usage:
        Single URL:
        ./fetch.py describe-url-metadata --urls="https://hopkinsresu.me"
        
        Multiple URLs:
        ./fetch.py describe-url-metadata --urls="https://hopkinsresu.me","https://autify.com"
   '''
    urls = urls.split(",")
    for url in urls:
        if url: fetch_utils.print_metadata(url)
    
if __name__ == '__main__':
    fire.Fire({
        'get-url': get_url,
        'describe-url-metadata': describe_url_metadata
    })