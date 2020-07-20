import globals as glob
from urllib.parse import quote
import urllib
from urllib import request
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


# def download_book(book, path=""):
#    know_better_book(book)
#    return

def get_soup(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    html_doc = mybytes.decode("utf8")
    fp.close()
    return BeautifulSoup(html_doc, 'html.parser')


def setup_proxy(proxy=None):
    if proxy == None:  # Use system default setting
        proxy_support = request.ProxyHandler()
    elif proxy == '':  # Don't use any proxy
        proxy_support = request.ProxyHandler({})
    else:  # Use proxy
        proxy_support = request.ProxyHandler(
            {'http': '%s' % proxy, 'https': '%s' % proxy})
    opener = request.build_opener(proxy_support)
    request.install_opener(opener)


proxy = []
with open("proxy.txt", "r") as myfile:
    data = myfile.readlines()
    for each in data:
        proxy.append(each.replace('\n', '').replace('\r', ''))


def download_book(book, path=""):
    for p in proxy:
        print('setting proxy for %s' % p)
        setup_proxy(p)
        try:
            print("getting download link")
            url = get_soup(sites[book['Type']] + book['Link']
                           ).find('a', class_="addDownloadedBook")['href']
            print(url)
            print("downloading from link")
            file_name = path + \
                "[{0}] {1}.{2}".format(
                    book['Author'], book['Name'], book["Format"])
            urllib.request.urlretrieve(url, file_name)
            wrong = False
            file1 = open(file_name, 'r')
            count = 0
            lines = []
            while True:
                count += 1
                line = file1.readline()
                if not line or count > 2:
                    break
                lines.append(line.strip())
            if lines[1].find("DOCTYPE") or lines[0].find("DOCTYPE"):
                wrong = True
            file1.close()
            if wrong:
                print("IP have limit")
                continue
            else:
                print("done!")
                break
        except:
            print("proxy doesn't work. Retry")
            continue


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
            new_book["Language"] = result.find('div', class_="property_language").find(
                "div", class_="property_value").string
        except:
            new_book["Language"] = "unknown"
        l.append(new_book)
    return l


def get_zlib_by_tag(tag, type="books"):
    books = []
    for page in range(1, 11, 1):
        link = sites[type] + ("/fulltext/{0}/?type=phrase&e=1&page={1}".format(quote(
            tag), page) if len(tag.split()) > 1 else "/s/{0}?page={1}/10".format(quote(tag), page))
        print("Openning page " + str(page) + " - " + link)
        books = books + get_results(glob.get_soup(link), type)
    return books


library = get_zlib_by_tag("Математические преобразования")
__count = 0
for b in library:
    download_book(b)
    __count = __count + 1
    if __count > 4:
        break
