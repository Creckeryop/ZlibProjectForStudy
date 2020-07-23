from __future__ import print_function
import six
import httplib2
from googleapiclient.discovery import build
import googleapiclient.http
import oauth2client.client


class GDrive:
    def __init__(self):
        # OAuth 2.0 scope that will be authorized.
        OAUTH2_SCOPE = 'https://www.googleapis.com/auth/drive'

        # Location of the client secrets.
        CLIENT_SECRETS = 'credentials.json'

        # Perform OAuth2.0 authorization flow.
        while True:
            try:
                flow = oauth2client.client.flow_from_clientsecrets(CLIENT_SECRETS, OAUTH2_SCOPE)
                flow.redirect_uri = oauth2client.client.OOB_CALLBACK_URN
                authorize_url = flow.step1_get_authorize_url()
                print('Go to the following link in your browser: ' + authorize_url)
                # `six` library supports Python2 and Python3 without redefining builtin input()
                code = six.moves.input('Enter verification code: ').strip()
                credentials = flow.step2_exchange(code)

                # Create an authorized Drive API client.
                http = httplib2.Http()
                credentials.authorize(http)
                self.drive_service = build('drive', 'v2', http=http)
                break
            except BaseException as e:
                print("Ошибка " + e + ". Устраните и попробуйте снова.")
                _ = input()
                continue

    def Upload(self, FILENAME='document.txt'):
        # тело вызова
        body = {
            'title': FILENAME,
            'description': 'from zlibrary',
        }
        # Права
        permissions = {
            'role': 'reader',
            'type': 'anyone'
        }
        while True:
            try:
                media_body = googleapiclient.http.MediaFileUpload(
                    FILENAME,
                    # mimetype='text/plain',
                    resumable=True
                )
                # Загружаем файл
                new_file = self.drive_service.files().insert(
                    body=body, media_body=media_body).execute()
                url = new_file.get('webContentLink')
                # Сделать файл общедоступным
                _ = self.drive_service.permissions().insert(body=permissions, fileId=new_file.get('id')).execute()
                print(FILENAME + " загружен. Ссылка: " + url)
                return url
            except BaseException as e:
                print("Ошибка " + e + ". Устраните и попробуйте снова.")
                _ = input()
                continue
