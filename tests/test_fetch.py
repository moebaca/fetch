"""Basic tests for the fetch."""

import os
import re
import fetch
import lib.fetch_utils

URL = 'https://autify.com'

def test_get_url():
    '''Runs get-url function and ensures HTML file creation.'''
    fetch.get_url(URL)
    os.path.isfile(lib.fetch_utils.get_url_file_path(URL))

def test_describe_url_metadata(capsys):
    '''Runs describe-url-metadata function and tests console output.'''
    fetch.describe_url_metadata(URL)
    captured = capsys.readouterr()
    assert re.search('num_links', captured.out)
    assert re.search('images', captured.out)
    assert re.search('last_fetch', captured.out)