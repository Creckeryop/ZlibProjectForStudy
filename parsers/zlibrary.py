import urllib
from urllib.parse import quote
from urllib import request
from bs4 import BeautifulSoup
import sys
import math

proxy = []

sites = {
    "articles": "https://booksc.xyz",
    "books": "https://b-ok.cc"
}

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'


def delete_last_line():
    sys.stdout.write(CURSOR_UP_ONE)
    sys.stdout.write(ERASE_LINE)


downloaded = 0
bar = None


def progress_bar(count, chunk_size, total_size):
    global downloaded, bar
    if bar is None:
        bar = 0
    else:
        delete_last_line()
    downloaded = downloaded + chunk_size
    bar = downloaded / total_size
    print("%s%% [%s/%s]" % (str(math.ceil(min(100, max(bar*100, 0)))), downloaded, total_size))


def setupProxy(proxy=None):
    if proxy == None:
        proxy_support = request.ProxyHandler()
    elif proxy == '':
        proxy_support = request.ProxyHandler({})
    else:
        proxy_support = request.ProxyHandler(
            {'http': '%s' % proxy, 'https': '%s' % proxy})
    opener = request.build_opener(proxy_support)
    request.install_opener(opener)

def loadProxy():
    with open("proxy.txt", "r") as myfile:
        data = myfile.readlines()
        for each in data:
            proxy.append(each.replace('\n', '').replace('\r', ''))


def checkHtml(filename):
    f = open(filename)
    try:
        f.readline()
        line2 = f.readline().find("!DOCTYPE")
        f.close()
        return line2 != -1
    except:
        f.close()
        return False


def getSoup(url):
    fp = request.urlopen(url, timeout=5)
    mybytes = fp.read()
    html_doc = mybytes.decode("utf8")
    fp.close()
    return BeautifulSoup(html_doc, 'html.parser')


def getResults(soup, t):
    l = []
    for result in soup.findAll("div", {"class": "resItemBox"}):
        book_info = result.find('h3', itemprop="name").a
        new_book = {
            "Author": result.find("div", class_="authors").a.string,
            "Name": book_info.string,
            "Link": sites[t] + book_info['href'],
            "Type": t,
            "Format": result.find('div', class_="property__file").find(
                "div", class_="property_value").string.split(', ')[0],
            "Size": result.find('div', class_="property__file").find(
                "div", class_="property_value").string.split(', ')[1],
        }
        try:
            new_book["Language"] = result.find('div', class_="property_language").find(
                "div", class_="property_value").string
        except:
            new_book["Language"] = "unknown"
        l.append(new_book)
    return l


def getByTag(tag, t="books"):
    books = []
    link = sites[t] + (("/fulltext/{0}/?type=phrase&e=1&page=" if len(
        tag.split()) > 1 else "/s/{0}?page=").format(quote(tag)))
    print("Парсинг списка %s!" % ("книг" if t == "books" else "статей"))
    for page in range(1, 11):
        books = books + getResults(getSoup(link + str(page)), t)
    return books


def downloadBook(book, folder_path=""):
    global proxy, downloaded, bar
    counter = 0
    file_name = ""
    end_prog = True
    while True:
        for p in proxy:
            print('Установка прокси: %s' % p)
            setupProxy(p)
            try:
                print("Получение ссылки на загрузку")
                url = getSoup(book['Link']).find(
                    'a', class_="addDownloadedBook")['href']
                print("Загрузка файла по ссылке ("+sites['books'] + url+"). Размер: %s" % book['Size'])
                downloaded = 0
                bar = None
                file_name = folder_path + ("[{0}] {1}.{2}".format(book['Author'], book['Name'], book["Format"])).replace(':', '').replace(
                    '*', '').replace('?', '').replace('/', '').replace('\\', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
                urllib.request.urlretrieve(
                    sites['books'] + url, file_name, progress_bar)
                delete_last_line()
                print("Файл загружен! [%s]" % file_name)
                if checkHtml(file_name):
                    counter = counter + 1
                    print("Прокси достигло лимита. Повтор")
                    continue
                else:
                    break
            except:
                print("Прокси не подходит. Повтор")
                counter = counter + 1
                continue
        if counter < len(proxy):
            proxy = proxy[counter:]
        else:
            proxy = []
        if len(proxy) == 0:
            print("Прокси закончилось!")
            while True:
                print("Загрузите новое прокси в proxy.txt файл [Y - чтобы продолжить / n - закончить работу программы]")
                s = input()
                if s == 'N' or s == 'n' or s == "Y" or s == "y":
                    if s == 'Y' or s=='y':
                        loadProxy()
                        end_prog = False
                    break
        if end_prog:
            break
            
    return file_name

def checkProxy():
    return len(proxy) > 0