import urllib
from urllib.parse import quote
from urllib import request
from bs4 import BeautifulSoup

proxy = []

tags = ['Киберфизические системы', 'Цифровая экономика', 'Индустрия 4.0', 'Умные системы', 'Интернет людей', 'Интернет вещей', 'Интернет сервисов', 'Архитектура киберфизической системы', 'Разнородность данных в киберфизической системе', 'Надежность в киберфизической системе', 'Управление данными в киберфизической системе', 'Конфиденциальность в киберфизической системе', 'Безопасность в киберфизической системе', 'Реальное время в киберфизической системе']

sites = {
    "articles": "https://booksc.xyz",
    "books": "https://b-ok.cc"
}


def setup_proxy(proxy=None):
    if proxy == None:
        proxy_support = request.ProxyHandler()
    elif proxy == '':
        proxy_support = request.ProxyHandler({})
    else:
        proxy_support = request.ProxyHandler(
            {'http': '%s' % proxy, 'https': '%s' % proxy})
    opener = request.build_opener(proxy_support)
    request.install_opener(opener)


def get_soup(url):
    fp = urllib.request.urlopen(url, timeout=5)
    mybytes = fp.read()
    html_doc = mybytes.decode("utf8")
    fp.close()
    return BeautifulSoup(html_doc, 'html.parser')


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
        books = books + get_results(get_soup(link), type)
    return books

# main


# Загружаем прокси для Z-library
with open("proxy.txt", "r") as myfile:
    data = myfile.readlines()
    for each in data:
        proxy.append(each.replace('\n', '').replace('\r', ''))

# Спарсим по тегам
library = get_zlib_by_tag(tags[1])
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

def download_book(book, path=""):
    global proxy
    counter = 0
    for p in proxy:
        print('setting proxy for %s' % p)
        setup_proxy(p)
        try:
            print("getting download link")
            url = get_soup(book['Link']).find('a', class_="addDownloadedBook")['href']
            print(url)
            print(sites['books'] + url)
            print("downloading from link")
            file_name = path + (\
                "[{0}] {1}.{2}".format(
                    book['Author'], book['Name'], book["Format"])).replace(':','').replace('*','').replace('?','').replace('/','').replace('\\','').replace('"','').replace('<','').replace('>','').replace('|','')
            urllib.request.urlretrieve(sites['books'] + url, file_name)
            print("done!")
            if check_html(file_name):
                counter = counter + 1
                continue
            else:
                break
        except:
            print("proxy doesn't work. Retry")
            counter = counter + 1
            continue
    if counter < len(proxy):
        proxy = proxy[counter:]
print(library[0])
download_book(library[0])
print(proxy)