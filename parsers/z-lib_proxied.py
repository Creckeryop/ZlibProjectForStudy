import urllib
from urllib.parse import quote
from urllib import request
from bs4 import BeautifulSoup


def get_soup(url):
    fp = urllib.request.urlopen(url, timeout=5)
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


sites = {
    "articles": "https://booksc.xyz",
    "books": "https://b-ok.cc"
}


def download_book(link):
    for p in proxy:
        print('setting proxy for %s' % p)
        setup_proxy(p)
        try:
            print("getting download link")
            url = get_soup(link).find('a', class_="addDownloadedBook")['href']
            print(url)
            print(sites['books'] + url)
            print("downloading from link")
            file_name = "book1.pdf"
            urllib.request.urlretrieve(sites['books'] + url, file_name)
            print("done!")
            if check_html(file_name):
                continue
            else:
                break
        except:
            print("proxy doesn't work. Retry")
            continue

def check_html(filename):
    f = open(filename)
    try:
        f.readline()
        line2 = f.readline().find("!DOCTYPE")
        f.close()
        return line2 != -1
    except:
        f.close()
        return False

# print(check_html("book3.pdf"))
download_book('https://b-ok.cc/book/4136263/891735?dsource=mostpopular')
