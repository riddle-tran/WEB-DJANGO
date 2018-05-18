from __future__ import unicode_literals
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from django.shortcuts import render,redirect
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from django.http import HttpResponse, HttpResponseRedirect
import os,io
import json
from apiclient import discovery
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from django.core.exceptions import ObjectDoesNotExist
from .upload import UploadFileForm
from .models import Music,CredentialsModel,Forder,Username,Musicid
from LSBweb.settings import GOOGLE_OAUTH2_CLIENT_SECRETS_JSON as jsondrive


import wave         # Python rocks!
import struct
import sys


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# Create your views here.
#Folder ID: 1M1Y0qU3qVcNYKeOB9Wa40o20CxnbLSfk
CLIENT_SECRETS_FILE =jsondrive
SCOPES = ['https://www.googleapis.com/auth/drive']

def kiemtra():
    try:
        q=CredentialsModel.objects.get(pk=11)
        credentials = q.cred
        drive = discovery.build('drive', 'v3', credentials=credentials)
        return drive 
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/oauth/')

def listFiles():
    drive = kiemtra()
    ID='1M1Y0qU3qVcNYKeOB9Wa40o20CxnbLSfk in parents'
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
    drive =kiemtra()
    file_metadata = {
    'name': user,
    'mimeType': 'application/vnd.google-apps.folder'}
    file = drive.files().create(body=file_metadata,fields='id').execute()
    print ('Folder ID: %s' % file.get('id'))
    p=Forder.objects.create(user=user,ma=file.get('id'))

def uploadFile(filename,user=None,folder_id='1M1Y0qU3qVcNYKeOB9Wa40o20CxnbLSfk'):#filename ten file luu lai
    drive=kiemtra()
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
    drive=kiemtra()
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
    lsb_watermark(filename, user, filename)
    uploadFile(filename,user,folder_id)



def index(request):    
    try:
        form = UploadFileForm()
        q=CredentialsModel.objects.get(pk=1)
        credentials = q.cred
        drive = discovery.build('drive', 'v3', credentials=credentials)
        listFiles()
        #createFolder("n14dcat011")
        #music=Music.objects.get(pk=1)
      #  file_id=music.ma
       # filename=music.tenbai
       # user=request.session['user']
       # id=Forder.objects.get(user=user)
       # folder_id=id.ma
       # downloadFile(file_id,filename,user, folder_id)
        return render(request, 'upload.html', {'form':form})   
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/oauth/')
    

def upload(f): 
    print "aaaaaaaaaaaaaaaaa"
    print f.name
    file = open(f.name, 'wb+') 
    for chunk in f.chunks():
        file.write(chunk)


def oauth(request):
    request.session['state'] =None
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri ='http://localhost:8000/oauth2callback'
    authorization_url, state = flow.authorization_url(
     access_type='offline',include_granted_scopes='true')
    request.session['state'] = state
    return redirect(authorization_url)
    

def oauth2callback(request):
    global credentials
    state = request.session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri ='http://localhost:8000/oauth2callback'
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    q=CredentialsModel(cred=credentials)
    q.save()
    return HttpResponseRedirect('/index/')







def lsb_watermark(cover_filepath, watermark_data, watermarked_output_path):
    
    watermark_str = str(watermark_data)
    watermark = struct.unpack("%dB" % len(watermark_str), watermark_str)
    
    watermark_size = len(watermark)
    watermark_bits = watermark_to_bits((watermark_size,), 32)
    watermark_bits.extend(watermark_to_bits(watermark))
    filepath="upload/" + cover_filepath
    cover_audio = wave.open(filepath, 'rb') 
    
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = cover_audio.getparams()
    frames = cover_audio.readframes (nframes * nchannels)
    samples = struct.unpack_from ("%dh" % nframes * nchannels, frames)

    if len(samples) < len(watermark_bits):
        raise OverflowError("The watermark data provided is too big to fit into the cover audio! Tried to fit %d bits into %d bits of space." % (len(watermark_bits), len(samples))) 
    
    print "Watermarking %s (%d samples) with %d bits of information." % (cover_filepath, len(samples), len(watermark_bits))
    
    encoded_samples = []
    
    watermark_position = 0
    n = 0
    for sample in samples:
        encoded_sample = sample
        
        if watermark_position < len(watermark_bits):
            encode_bit = watermark_bits[watermark_position]
            if encode_bit == 1:
                encoded_sample = sample | encode_bit
            else:
                encoded_sample = sample
                if sample & 1 != 0:
                    encoded_sample = sample - 1
                    
            watermark_position = watermark_position + 1
            
        encoded_samples.append(encoded_sample)
            
    encoded_audio = wave.open(watermarked_output_path, 'wb')
    encoded_audio.setparams( (nchannels, sampwidth, framerate, nframes, comptype, compname) )

    encoded_audio.writeframes(struct.pack("%dh" % len(encoded_samples), *encoded_samples))

def watermark_to_bits(watermark, nbits=8):
    watermark_bits = []
    for byte in watermark:
        for i in range(0,nbits):
            watermark_bits.append( (byte & (2 ** i)) >> i )
    return watermark_bits
    
def recover_lsb_watermark(watermarked_filepath):
    # Simply collect the LSB from each sample
    watermarked_audio = wave.open(watermarked_filepath, 'rb') 
    
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = watermarked_audio.getparams()
    frames = watermarked_audio.readframes (nframes * nchannels)
    samples = struct.unpack_from ("%dh" % nframes * nchannels, frames)
    
    # determine how many watermark bytes we should look for
    watermark_bytes = 0
    for (sample,i) in zip(samples[0:32], range(0,32)):
        watermark_bytes = watermark_bytes + ( (sample & 1) * (2 ** i))
    
    print "Recovering %d bytes of watermark information from %s (%d samples)" % (watermark_bytes, watermarked_filepath, len(samples))
    
    watermark_data = []
    
    for n in range(0, watermark_bytes):
        watermark_byte_samples = samples[32 + (n * 8) : 32+((n+1) * 8)]
        watermark_byte = 0
        for (sample, i) in zip(watermark_byte_samples, range(0,8)):
            watermark_byte = watermark_byte + ( (sample & 1) * (2**i) )
        watermark_data.append(watermark_byte)
            
    return watermark_data
    
def watermark_to_string(list):
    return "".join([chr(x) for x in list])

def embed_file(cover_audio, hidden_file, output):
	f = open(hidden_file)
	hidden_data = f.read()
	lsb_watermark(cover_audio, hidden_data, output)

def recover_embedded_file(encoded_signal, hidden_data_dest):
	wm = recover_lsb_watermark(encoded_signal)
	wm_str = watermark_to_string(wm)
	f = open(hidden_data_dest,"w")
	f.write(wm_str)
    

