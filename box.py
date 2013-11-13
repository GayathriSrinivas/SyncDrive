#! /usr/bin/python

import json
import os
import requests
import db_util
import urllib
import urllib2

label = 'box'
display_label = 'Box'
oauth_url = 'https://www.box.com/api/oauth2/authorize?response_type=code&client_id=3r1kni75hifxne62zectnok8ar5brsh2&state=authenticated'

def download_file(file_id,email):
	access_token = db_util.fetch_access_token(email,label)
	#Get the Raw file content
	response = requests.get("https://api.box.com/2.0/files/%(file_id)s/content?access_token=%(access_token)s" % locals())
	#Get the name of the file
	raw_data = requests.get("https://api.box.com/2.0/files/%(file_id)s?access_token=%(access_token)s" % locals()).json()
	filename = os.path.join('/tmp', raw_data.get('name', 'file'))
	f = open(filename, 'w')
	f.write(response.content)
	f.close()
	return filename

def upload_file(filename,email):
	access_token = db_util.fetch_access_token(email,label)
	url = 'https://upload.box.com/api/2.0/files/content?access_token=%(access_token)s' % locals()
	r = requests.post(url, files={'file': open(filename, 'rb') } ,data = { 'parent_id': '0' })
	print "###" ,r.text ,"###"

def list_files(email,folder):
	access_token = db_util.fetch_access_token(email,label)
	folder = folder if folder else '0'
	url = "https://api.box.com/2.0/folders/%(folder)s/items?access_token=%(access_token)s" % locals()
	response = requests.get(url).json()
	files = []
	for record in response["entries"]:
		fileRecord = {}
		fileRecord["id"]=record["id"]
		fileRecord["name"]=record["name"]
		fileRecord["link"]=record.get("download_url","")
		fileRecord["size"]=record.get("fileSize","")
		fileRecord["is_folder"] = (record.get("type", '') == 'folder')
		files.append(fileRecord)
	return files


if __name__ == "__main__":
	#print list_files('gaya.0408@gmail.com')
	#print download_file('11673767837','gaya.0408@gmail.com')
	upload_file('templates/entry.html','gaya.0408@gmail.com')
	print 'done :)'
