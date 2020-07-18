import globals as glob
from urllib.parse import quote
import urllib
from bs4 import BeautifulSoup

sites = {
    "articles": "https://booksc.xyz",
    "books": "https://b-ok.cc"
}


def know_better_book(book):
    soup = glob.get_soup(book["Link"])
    book['DownloadLink'] = sites[book["Type"]] + \
        soup.find('a', class_="addDownloadedBook")['href']


def get_download_link(book):
    if not ('DownloadLink' in book):
        know_better_book(book)
    return book['DownloadLink']


def download_book(book, path=""):
    return urllib.request.urlretrieve(get_download_link(book), path + "[{0}] {1}.{2}".format(book['Author'], book['Name'], book["Format"]))


def get_results(soup, type):
    l = []
    for result in soup.findAll("div", {"class": "resItemBox"}):
        book = result.find('h3', itemprop="name").a
        new_book = {
            "Author": result.find("div", class_="authors").a.string,
            "Name": book.string,
            "Link": sites[type] + book['href'],
            "Type": type,
            "Format": result.find('div', class_="property__file").find(
                "div", class_="property_value").string.split(',', 1)[0],
            
        }
        try:
            new_book["Language"] = result.find('div', class_="property_language").find("div", class_="property_value").string
        except:
            new_book["Language"] = "unknown"
        l.append(new_book)
    return l


def get_zlib_by_tag(tag, type="books"):
    books = []
    for page in range(1, 10, 1):
        print("Openning page " + str(page))
        books = books + get_results(glob.get_soup(
            sites[type] + "/s/{0}?page={1}/10".format(quote(tag), page)), type)
    return books


print(get_zlib_by_tag("Математика"))
    