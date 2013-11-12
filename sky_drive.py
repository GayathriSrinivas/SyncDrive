#! /usr/bin/python

import json
import requests
import os
import db_util

label = 'sky_drive'
display_label = 'Skydrive'
oauth_url = 'https://login.live.com/oauth20_authorize.srf?client_id=0000000048104E79&scope=wl.skydrive,wl.skydrive_update,wl.offline_access&response_type=token&redirect_uri=http://ec2.socialphotos.net:5000/callback'
#oauth_url = 'https://login.live.com/oauth20_authorize.srf?client_id=0000000048104E79&scope=wl.skydrive,wl.skydrive_update,wl.offline_access&response_type=code&redirect_uri=http://ec2.socialphotos.net:5000/callback'

def upload_file(filename, email):
	access_token = db_util.fetch_access_token(email,label)
	url = 'https://apis.live.net/v5.0/me/skydrive/files?access_token=%(access_token)s' % locals()
	r = requests.post(url, files={'file': open(filename, 'rb')})
	print r.text

def download_file(file_id, email):
	access_token = db_util.fetch_access_token(email,label)
	raw_data = requests.get("https://apis.live.net/v5.0/%(file_id)s?access_token=%(access_token)s)" % locals()).json()
	filename = os.path.join('/tmp', raw_data.get('name', 'file'))
	data = requests.get('%s&access_token=%s' % (raw_data['source'], access_token))
	f = open(filename, 'w')
	f.write(data.content)
	f.close()
	return filename

def list_files(email,folder):
	access_token = db_util.fetch_access_token(email,label)
	url = "https://apis.live.net/v5.0/me/skydrive/files?access_token=%(access_token)s" % locals()
	if folder:
		url = "https://apis.live.net/v5.0/%(folder)s/files?access_token=%(access_token)s" % locals()
	response = requests.get(url).json()
	listFiles = []
	for record in response["data"]:
		fileRecord = {}
		fileRecord["id"]=record["id"]
		fileRecord["name"]=record["name"]
		fileRecord["link"]=record.get("source","")
		fileRecord["size"]=record["size"]
		fileRecord["is_folder"] = (record['id'].split('.')[0] == "folder")
		listFiles.append(fileRecord)
	return listFiles

if __name__ == '__main__':
	download_file('file.5d1d0df0479ac5c9.5D1D0DF0479AC5C9!250', 'gaya.0408@gmail.com')
	#print list_files('gaya.0408@gmail.com','folder.5d1d0df0479ac5c9.5D1D0DF0479AC5C9!154')
	#sd_download_file('file.5d1d0df0479ac5c9.5D1D0DF0479AC5C9!250','EwAwAq1DBAAUGCCXc8wU/zFu9QnLdZXy+YnElFkAAcLvq3EQeMCRAIx5zKMNY0DGK2I6P8vBDknDU61fE9lHvNRLTh01fVJ5v8d6MlYjsUOdd9iKs/wTwSlvy+mfhOYQ3IoBGpcYEJPaIrnQRMC9oRCJR3iWwXUqYdvsbS+5fl5t0qsyie397D1P9GbEkI2H1nqHWEBBVO7IcTMrP1Gb0mO5aS4osoqQ/mTKTa5015hNwDyK1VTcsJ9sj9oBYJNA3K7BYmb9wxmIrBVXBFdNZ2AP1dTxZ0qZmjUppD5dltA+VIr+77MZdIQpDGjbE9x1mRRyCFyoTw0tXLEouJhYjru6enY2P68qEDSbgqFBywecrfkgm4tBKAYGNZkgn50DZgAACKe4tSkAEtApAAG6FvWB7ijA190ANcBl27YUc6uN5/ulvZUDoNPrY5zvKwGHZCY4uhTi4sYG63loo/k0cXHy6lPqjPNf4e9U4rOdMxPY5eXPVDD0gBHO9DbdeLmukf1YuHKrK9koYL05X/CD8dLq3aN9CQEyRFoviDj9DggAJ+RB+zaIDZ2mOZgXDWrgRUNh704ykjQ7Y5PhH3T9Zj7XSHcRSrZzCgJYp0UFzNJEpblyqarSd/ftk2mXMaid3h8STXXX6rabVi9mXLvbVdTHyjOLipfmydzjss0y6w6q5mp+cecgv8JZkp4cWU0cMRHDKSisPdpMW0tezpCKr3Q8N0nrwWYMiS9W5khpAAA=')
	#sd_upload_file('/tmp/aws-sjsu-key.pem', 'EwAwAq1DBAAUGCCXc8wU/zFu9QnLdZXy+YnElFkAAdyvyBb7dUPxcs+A1eORq0kZnQIgSUTNNRYRjw/qIiE7we3Wav687rdfgopEaXnhAvtLflwrpm7hucVvIyVgJx7ODJqrLEDPyyrnLpUE0HO2iQvDlF5DSwHw7a57xGEomEV81W0m8HsbynxtThpBNXnR6q9i1FD+tjSM7oyiPl/J9Ofm1nKOp6UtZs8qSkHRm1Bc4bFHsjLCCPy+/hsUnl4IocvVdy6FUf96NuK7//K2+vXkFEAagbi0OLQN+WtSOGhCmvAbb942dQCD4ohBjp67XCydwH5TOnw46/EuEkke5zD3k5b1CfN0/+BBT8xidUx6uaSVZGyI+Tn2EarlBhADZgAACBYCLb9tTOrAAAHDfT3nq5PVIetO7cOoGCd+jXTM0qlcpvmUECG84a4veXM+95BExZviaVFbeTv4ASyfh9MI/iD5pAWwVhy9M0nbcGa27bP3rgtpg2Wc2ussBATPEQ8w9UxZrQdiE0WGhHwIdLnHSdYXzfYl8jGGDtJ/FbXqW1FXgjzV7PUginbj9GrAbwYda4CszDg98DRKlJWW3nBd8l6ycbdcx2xH/WnSu4v6M1jgRrd55sLUj4FwELXrVOgqVl0zE3JRchvyWFuVD+doFWwIPW4lWPaBsqJZ1Ax4rQ5QuVzBK8wSqFBKSP7zx+/1RmMF3zT6TX14AugMmTITSyS4FTctQ9nfQ/eOAAA=')