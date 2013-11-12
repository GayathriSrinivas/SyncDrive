#! /usr/bin/python

import json
import os
import requests
import db_util
import urllib

label = 'google_drive'
display_label = 'Google Drive'
oauth_url = 'https://accounts.google.com/o/oauth2/auth?scope=https://www.googleapis.com/auth/drive&redirect_uri=http://ec2.socialphotos.net:5000/callback_google&response_type=code&client_id=485476280210.apps.googleusercontent.com&access_type=offline'

def download_file(file_id,email):
	access_token = db_util.fetch_access_token(email,label)
	raw_data = requests.get("https://www.googleapis.com/drive/v2/files/%(file_id)s?access_token=%(access_token)s" % locals()).json()
	filename = os.path.join('/tmp', raw_data.get('title', 'file'))
	f = open(filename, 'w')
	data = requests.get('%s&access_token=%s' % (raw_data['downloadUrl'], access_token))
	f.write(data.content)
	f.close()
	return filename

def upload_file(filename,email):
	access_token = db_util.fetch_access_token(email,label)
	url = 'https://www.googleapis.com/upload/drive/v2/files?uploadType=media&access_token=%(access_token)s' % locals()
	r = requests.post(url, data = open(filename, 'rb').read())
	file_id = json.loads(r.text)['id']
	url = "https://www.googleapis.com/drive/v2/files/%(file_id)s?access_token=%(access_token)s" % locals()
	r = requests.put(url, 
				     data = json.dumps({'title': os.path.basename(filename)}),
				     headers = {'Content-Type': "application/json"})
	print r.text

def list_files(email,folder):
	access_token = db_util.fetch_access_token(email,label)
	folder = folder if folder else 'root'
	query = urllib.quote("\'%(folder)s\' in parents" % locals())
	url = "https://www.googleapis.com/drive/v2/files?access_token=%(access_token)s&q=%(query)s" % locals()
	print url
	response = requests.get(url).json()
	print response
	files = []
	for record in response["items"]:
		fileRecord = {}
		fileRecord["id"]=record["id"]
		fileRecord["name"]=record["title"]
		fileRecord["link"]=record.get("webContentLink","")
		fileRecord["size"]=record.get("fileSize","")
		fileRecord["is_folder"] = (record.get("mimeType", '') == 'application/vnd.google-apps.folder')
		files.append(fileRecord)
	return files

if __name__ == "__main__":
	print list_files('gaya.0408@gmail.com')
	#print gd_download_file('0B2xo1MFqnLo5dUtfRHVMbExvZWc','ya29.AHES6ZTZz8XGWDowjsgQs8InH5BKFxuFCaBDcr2JCkLbFjQ7Ww')
	#gd_upload_file('templates/hello.html','ya29.AHES6ZQIKpE9Cbypa1jLXGtlmJAZqFMYz5cvlpFwfn5zpq7kMFUDcVnj')
	print 'done :)'
