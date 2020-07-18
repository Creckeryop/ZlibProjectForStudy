from bs4 import BeautifulSoup
import urllib.request
def get_soup(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    html_doc = mybytes.decode("utf8")
    fp.close()
    return BeautifulSoup(html_doc, 'html.parser')