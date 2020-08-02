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


#ИНТЕРФЕЙС ПОЛЬЗОВАТЕЛЯ
#================================================================================================
#главное окно программы
root = Tk()

focusIndex = 0

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
sf2.pack(side="top", expand=0)
sf2.bind_arrow_keys(root)
sf2.bind_scroll_wheel(root)
frame_authors = sf2.display_widget(Frame, True)

#значения выпадающего списка
arrAuth = ["author1","author2","author3","author4", "author5", "author6"]

#количество значений в списке(нужно для программы)
length1 = len(arrAuth)

#массив булеан значений, сопоставляемый списку
boolArrAuth = []
for i in range(0, length1):
    boolArrAuth.append(BooleanVar())
    boolArrAuth[i].set(0)

#добавление на экран флажков
for i in range(0, length1):
    checkbox = Checkbutton(frame_authors, text = arrAuth[i], variable = boolArrAuth[i], onvalue=1, offvalue=0)
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
sf1.pack(side="top", expand=0)
sf1.bind_arrow_keys(root)
sf1.bind_scroll_wheel(root)
frame_keywords = sf1.display_widget(Frame, True)

#значения выпадающего списка
arr = ["punkt1","punkt2","punkt3","punkt4", "punkt5", "punkt6"]

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
def printArticle(author, theme, name, link, inner_frame):
    Label(inner_frame, text =\
    "АВТОР: "+author+"\n\n"+\
    "ТЕМА:"+theme+"\n\n"+\
    "НАЗВАНИЕ:"+name+" \n",\
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
def getAuthors(boolArrAuth):
    checkedItems = []
    checkedItems.clear()
    for i in range(0, length1):
        if boolArrAuth[i].get()==1:
            checkedItems.append(arrAuth[i])
    return checkedItems

#ссылки для пересоздания прокручиваемого фрейма
#Создание прокручиваемого блока
sf = ScrolledFrame(root, width=640, height=480, highlightthickness=5, highlightbackground="#ffffff")
sf.pack(side="top", expand=1, fill="both")
sf.bind_arrow_keys(root)
sf.bind_scroll_wheel(root)
inner_frame = sf.display_widget(Frame, True)

#функция-обработчик кнопки ПОИСКА
def beginSearch(event):
    global inner_frame
    global sf

    #удаление прокручиваемого блока, если он существует
    if(not(inner_frame is None)):
        inner_frame.destroy()
        sf.destroy()

    sf1.configure(highlightbackground="#ffffff")

    #Создание прокручиваемого блока
    sf = ScrolledFrame(root, width=640, height=480, highlightthickness=5, highlightbackground="red")
    sf.pack(side="top", expand=1, fill="both")
    sf.bind_arrow_keys(root)
    sf.bind_scroll_wheel(root)
    inner_frame = sf.display_widget(Frame, True)

    #параметры обработанных статей
    author = "author"
    theme = "theme"
    name = "name"
    link = "link"
    
    #themeInputted = inputTheme.get()
    authors_arrInputted = getAuthors(boolArrAuth)
    for s in authors_arrInputted:
        print(s+"\n")

    #получение массива выбранных ключевых слов
    keywords_arrInputted = getKeywords(boolArr)
    for s in keywords_arrInputted:
        print(s+"\n")

    for i in range(1,random.randint(0,16)):
        printArticle(author, theme, name, link, inner_frame)
    
#установка обработчика для кнопки поиска
searchButton.bind('<Button-1>', beginSearch)






#эту штуку надо в конец добавить
root.mainloop()