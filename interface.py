from tkinter import *
from tkscrolledframe import ScrolledFrame
import webbrowser
import urllib
from urllib import request
import random
import pyodbc

#обработчик кнопки ССЫЛКИ
def onClickLink(event):
    
     #получение ссылки на скачивание
     link = event.widget.cget("text")

     print(link)

     webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))

     webbrowser.get('chrome').open(link)


#ТЕРРИТОРИЯ БАЗЫ ДАННЫХ
#================================================================================================
#подключаем нашу базу данных
cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=(LocalDb)\\MSSQLLocalDB;"
                      "Database=LUL;"
                      "Trusted_Connection=yes;")
cursor = cnxn.cursor()

#функция для получения авторов из базы данных
def getDBAuthors():
    global cursor
    authors = ["ЛЮБОЙ"]
    cursor.execute("Select Distinct Author from Book")
    for i in cursor.fetchall():
        authors.append(i[0])
    return authors

#функция для получения списка тэгов книг из базы данных
def getDBKeywords():
    global cursor
    authors = []
    cursor.execute("Select Name from KeyWord")
    for i in cursor.fetchall():
        authors.append(i[0])
    return authors

#ИНТЕРФЕЙС ПОЛЬЗОВАТЕЛЯ
#================================================================================================
#главное окно программы
root = Tk()

focusIndex = 0

#функция-обработчик наведения на фрейм
def hoverFrame(event):
    #print("event.widget"+str(dir(event.widget)))
    global sf1, sf, sf2

    focusList = [sf1, sf, sf2]
    

    for i in range(0, (len(focusList))):
        #print("focuslist[]"+str(dir(focusList[i])))
        if  focusList[i].yview == event.widget.yview:
            focusList[i].configure(highlightbackground="red")
            focusList[i].bind_scroll_wheel(root)
            focusList[i].bind_arrow_keys(root)
        else:
            focusList[i].configure(highlightbackground="#ffffff")

#обработчик нажатия на первый фрейим
def changeFocus(event):

    global focusIndex, sf1, sf, sf2

    focusList = [sf1, sf, sf2]
    
    focusIndex = (focusIndex + 1) % len(focusList)

    for i in range(0, (len(focusList))):
        if i == focusIndex:
            focusList[i].configure(highlightbackground="red")
            focusList[i].bind_scroll_wheel(root)
        else:
            focusList[i].configure(highlightbackground="#ffffff")

root.bind('<Control_L>', changeFocus)

#подсказка для пользователя
Label(root, text="ПАРСЕР НАУЧНЫХ СТАТЕЙ", width = 75, height = 2, font="Arial 16").pack(pady = 15)

#первый фрейм
#------------------------------------------------------------------------------------------------
#fr1 = Frame(bg="#ffffff", width = 100)

#подсказка для пользователя
#Label(fr1, text = "Тема:", width = 30, height = 2, font = "Arial 13").pack(side = LEFT)

#поле ввода темы
#inputTheme = Entry(fr1, width = 70, font = "Arial 13")
#inputTheme.pack(ipady = 8)
#------------------------------------------------------------------------------------------------

#второй фрейм
#------------------------------------------------------------------------------------------------
fr2 = Frame(bg="#ffffff", width = 100)

#подсказка для пользователя
Label(fr2, text="Автор:", width = 100, height = 2, font="Arial 13").pack()

#Создание прокручиваемого блока для кчпичка авторов
sf2 = ScrolledFrame(fr2, width=880, height=100, highlightthickness=5, highlightbackground="#ffffff")
sf2.itemId=2
sf2.pack(side="top", expand=0)
sf2.bind_arrow_keys(root)
sf2.bind_scroll_wheel(root)
sf2.bind("<Enter>", hoverFrame)
frame_authors = sf2.display_widget(Frame, True)

#значения выпадающего списка
arrAuth = getDBAuthors()

#количество значений в списке(нужно для программы)
length1 = len(arrAuth)

#массив булеан значений, сопоставляемый списку
authorKey = IntVar()
authorKey.set(0)

#добавление на экран флажков
for i in range(0, length1):
    checkbox = Radiobutton(frame_authors, text = arrAuth[i], variable = authorKey, value=i)
    checkbox.pack()

#массив выбранных ключевых слов
checkedAuthItems = []
#------------------------------------------------------------------------------------------------

#третий фрейм
#------------------------------------------------------------------------------------------------

fr3 = Frame(bg="#ffffff", width = 100)

#подсказка для пользователя
Label(fr3, text="Ключевые слова:", width = 100, height = 2, font="Arial 13").pack()

#Создание прокручиваемого блока для кчпичка ключевых слов
sf1 = ScrolledFrame(fr3, width=880, height=100, highlightthickness=5, highlightbackground="red")
sf1.itemId=1
sf1.pack(side="top", expand=0)
sf1.bind_arrow_keys(root)
sf1.bind_scroll_wheel(root)
sf1.bind("<Enter>", hoverFrame)
frame_keywords = sf1.display_widget(Frame, True)

arr = getDBKeywords()

#количество значений в списке(нужно для программы)
length = len(arr)

#массив булеан значений, сопоставляемый списку
boolArr = []
for i in range(0, length):
    boolArr.append(BooleanVar())
    boolArr[i].set(0)

#добавление на экран флажков
for i in range(0, length):
    checkbox = Checkbutton(frame_keywords, text = arr[i], variable = boolArr[i], onvalue=1, offvalue=0)
    checkbox.pack()

#массив выбранных ключевых слов
checkedItems = []
#------------------------------------------------------------------------------------------------

#четвертый фрейм
#------------------------------------------------------------------------------------------------

fr4 = Frame(bg="#ffffff")

#кнопка поиска
searchButton = Button(fr4, width = 30, text="Искать", font="Arial 13")
searchButton.pack()
#------------------------------------------------------------------------------------------------

#код размещения элементов управления на экране
#fr1.pack(pady = 10)
fr2.pack(pady = 10)
fr3.pack(pady = 10)
fr4.pack(pady = 10)

#настройка цвета фона главного окна
root.configure(background='#c0c0c0', width = 100)

#================================================================================================

#функция, которая выводит на экран информацию о добавленных в БД статьях
def printArticle(author, name, link, language, file_format, inner_frame):
    Label(inner_frame, text =\
    "НАЗВАНИЕ: "+name+"\n\n"+\
    "АВТОР: "+author+"\n\n"+\
    "ЯЗЫК: "+language+"    "+\
    "ФОРМАТ: "+file_format,\
    width = 100, height = 10,font = "Arial 13").pack(pady = 2)
    linkButt = Button(inner_frame, width = 100, text=link, bg="#000000", fg="#ffffff", font="Arial 13")
    linkButt.bind('<Button-1>', onClickLink)
    linkButt.pack()
    
#функция, вычленяющая помеченные элементы из массива ключевых слов
def getKeywords(boolArr):
    checkedItems = []
    checkedItems.clear()
    for i in range(0, length):
        if boolArr[i].get()==1:
            checkedItems.append(arr[i])
    return checkedItems

#функция, вычленяющая помеченные элементы из массива авторов
def getAuthor(authorKey):
    return arrAuth[authorKey]

#ссылки для пересоздания прокручиваемого фрейма
#Создание прокручиваемого блока
sf = ScrolledFrame(root, width=640, height=480, highlightthickness=5, highlightbackground="#ffffff")

sf.pack(side="top", expand=1, fill="both")
sf.bind_arrow_keys(root)
sf.bind_scroll_wheel(root)
sf.bind("<Enter>", hoverFrame)
sf.itemId=0
inner_frame = sf.display_widget(Frame, True)

#функция-обработчик кнопки ПОИСКА
def beginSearch(event):
    global cursor
    global inner_frame
    global sf
    global authorKey
    #удаление прокручиваемого блока, если он существует
    if(not(inner_frame is None)):
        inner_frame.destroy()
        sf.destroy()

    sf1.configure(highlightbackground="#ffffff")

    #Создание прокручиваемого блока
    sf = ScrolledFrame(root, width=640, height=480, highlightthickness=5, highlightbackground="red")
    sf.itemId=0
    sf.pack(side="top", expand=1, fill="both")
    sf.bind_arrow_keys(root)
    sf.bind_scroll_wheel(root)
    sf.bind("<Enter>", hoverFrame)
    inner_frame = sf.display_widget(Frame, True)

    #параметры обработанных статей
    author = "author"
    theme = "theme"
    name = "name"
    link = "link"
    
    author_inputted = getAuthor(authorKey.get())
    print(author_inputted)
    keywords = []
    for s in getKeywords(boolArr):
        keywords.append(s)

    command = "select Book.Name,Book.Author,Book.Cloud_Link, Book.Language, Book.Format from Book"

    command += """\njoin BookKeyWord on Book.Id = BookKeyWord.Book_Id\njoin KeyWord on BookKeyWord.KeyWord_Id = KeyWord.Id"""
    if len(keywords) > 0:
        command = command + "\nwhere Keyword.Name = N'" + '\' and Keyword.Name = N\''.join(keywords) + "\'"
        if not (author_inputted == "ЛЮБОЙ"):
            command = command + " and Book.Author = N'" + author_inputted + "'"
    else:
        if not (author_inputted == "ЛЮБОЙ"):
            command = command + "\nwhere Book.Author = N'" + author_inputted + "'"
    print(command)
    cursor.execute(command)
    for book in cursor.fetchall():
        printArticle(book[1], book[0], book[2], book[3], book[4], inner_frame)
    """
    authors_arrInputted = getAuthors(boolArrAuth)
    for s in authors_arrInputted:
        print(s+"\n")

    #получение массива выбранных ключевых слов
    keywords_arrInputted = getKeywords(boolArr)
    for s in keywords_arrInputted:
        print(s+"\n")

    for i in range(1,random.randint(0,16)):
        printArticle(author, theme, name, link, inner_frame)
    #"""
    
#установка обработчика для кнопки поиска
searchButton.bind('<Button-1>', beginSearch)


#эту штуку надо в конец добавить
root.mainloop()