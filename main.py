from __future__ import print_function
import pickle
import pyodbc
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from parsers import zlibrary as Zlib
import googleDriveClass as Drive

# tags = ['Киберфизические системы', 'Цифровая экономика', 'Индустрия 4.0', 'Умные системы', 'Интернет людей', 'Интернет вещей', 'Интернет сервисов', 'Архитектура киберфизической системы', 'Разнородность данных в киберфизической системе',
#        'Надежность в киберфизической системе', 'Управление данными в киберфизической системе', 'Конфиденциальность в киберфизической системе', 'Безопасность в киберфизической системе', 'Реальное время в киберфизической системе']
tags = ['Киберфизические системы', 'Цифровая экономика',
        'Индустрия 4.0', 'Умные системы', 'Интернет людей']
# подключаемся к базе данных
cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=(LocalDb)\\MSSQLLocalDB;"
                      "Database=LUL;"
                      "Trusted_Connection=yes;")
cursor = cnxn.cursor()

# подключение к диску
uploader = Drive.GDrive()

# добавляем ключевые слова (tags) в бд

#cursor.execute("Delete from KeyWord")

# for tag in tags:
#    cursor.execute("Insert into KeyWord (Name) values (N'"+tag+"')")

# cnxn.commit()

Zlib.loadProxy()
for tag in tags:
    print("Тэг '%s'" % tag)
    library = Zlib.getByTag(tag)
    library.extend(Zlib.getByTag(tag, "articles"))
    for item in library:
        print("%s - Автор: %s" % (item['Name'], item['Author']))
        cursor.execute("if exists (Select * from book where book.Download_Link=N'"+str(item['Link']).replace("'", "")+"') " +
                       "select * from book")
        try:
            object_none = cursor.fetchone()[0]
        except:
            # Возможно нужно прежде чем скачивать, проверить на наличие этой книги в БД
            # Здесь уже нужно сделать загрузку файла который скачался
            # file_name путь к скаченной книге на диске
            file_name = Zlib.downloadBook(item)
            drive_url = uploader.Upload(FILENAME=file_name)
            cursor.execute("if not exists (Select * from KeyWord where KeyWord.Name = N'" +
                           tag+"') Insert into KeyWord (Name) values (N'"+tag+"')")
            cnxn.commit()
            cursor.execute("Insert into Book (Download_Link,Cloud_Link,Author,Name,Language,Format) " +
                           "values (N'"+str(item['Link']).replace("'", "")+"',"+"N'"+str(drive_url).replace("'", "")+"',N'"+str(item['Author']).replace("'", "")+"',N'"+str(item['Name']).replace("'", "")+"','"+str(item['Language']).replace("'", "")+"','"+str(item['Format']).replace("'", "")+"')")
        cursor.execute(
            "select book.Id from Book where book.Download_Link='"+str(item['Link'])+"'")
        book_id = cursor.fetchone()[0]
        print(book_id)
        cursor.execute(
            "select keyword.id from KeyWord where keyword.Name=N'"+tag+"'")
        keyword_id = cursor.fetchone()[0]
        cursor.execute("if not exists (select * from BookKeyWord where BookKeyWord.Book_Id = "+str(book_id)+" and BookKeyWord.KeyWord_Id = "+str(keyword_id)+") Insert into BookKeyWord (Book_Id, KeyWord_Id) values (" +
                       str(book_id)+","+str(keyword_id)+")")
        # сохраняем изменения в бд
        cnxn.commit()

        # Прокси закончилось, так что конец программы
        # Функция Zlib.downloadBook попросит дать ему новый прокси лист, если не хватит, так что не обращайте внимания на эти строки
        if not Zlib.checkProxy():
            break
