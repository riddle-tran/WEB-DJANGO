from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from django.core.exceptions import ObjectDoesNotExist
from .models import Music,Forder,Username,Musicid
import os,io
# Setup the Drive v3 API
SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
drive = build('drive', 'v3', http=creds.authorize(Http()))


def listFiles():
        results = drive.files().list(
        q="'1M1Y0qU3qVcNYKeOB9Wa40o20CxnbLSfk' in parents ",fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))
                q=Music(tenbai=item['name'],ma=item['id'])
                q.save()
def createFolder(user):
        file_metadata = {
        'name': user,
        'mimeType': 'application/vnd.google-apps.folder'}
        file = drive.files().create(body=file_metadata,fields='id').execute()
        p=Forder.objects.create(user=user,ma=file.get('id'))
    

def uploadFile(filename,user=None,folder_id='1M1Y0qU3qVcNYKeOB9Wa40o20CxnbLSfk'):#filename ten file luu lai
        filepath="upload/" + filename
        file_metadata = {'name': filename,
        'parents': [folder_id]}
        media = MediaFileUpload(filepath,mimetype='audio/wav')
        file = drive.files().create(body=file_metadata, media_body=media,fields='id').execute()
        if user==None:
            q=Music(tenbai=filename,ma=file.get('id'))
            q.save()
        else:
            Musicid.objects.create(user=user,tenbai=filename,ma=file.get('id'))

def downloadFile(file_id,filename,user, folder_id):
        request = drive.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        filepath="upload/" + filename
        with io.open(filepath,'wb') as f:
            fh.seek(0)
            f.write(fh.read())
        #lsb_watermark(filename, user, filename)
        uploadFile(filename,user,folder_id)

