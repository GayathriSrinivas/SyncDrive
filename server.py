from flask import *
import urllib2
import json
import requests
import urllib
import google_drive
import sky_drive
import db_util
import dropbox

SECRET_KEY = 'synergy'
app = Flask(__name__)
app.config.from_object(__name__)

def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def get_provider(index):
	mapping = {
				0 : google_drive,
				1 : sky_drive,
				2 : dropbox
			  }
	return mapping[index]


@app.route('/')
def welcome_page():
    return render_template('welcome.html')

@app.route('/sign_up')
def signup_page():
    return render_template('sign_up.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/entry',methods = ['POST'] )
def store_user():
	username = request.form['username']
	password = request.form['password']
	db_util.user_signup(username,password)
	session["email"] = username
	return redirect('/transfer')
	return render_template('entry.html',username=username,password=password)

#@app.route('/login')
#def input_page():
#	return render_template('login.html') 

# skydrive callback
@app.route('/callback')
def callback():
	return render_template('callback.html')

# skydrive access token callback
@app.route('/callback')
def skydrive_access_token():
	access_token = request.args.get('token','')
	db_util.save_access_token(access_token, 'sky_drive', session['email'])
	return redirect('/transfer')

@app.route('/callback_google')
def callback_google():
 	code = request.args.get('code')
	values = {
            'code':code,
            'client_id':'485476280210.apps.googleusercontent.com' ,
            'client_secret':'I_fk8bSDc0S2mjaGuJcV3k-6',
            'redirect_uri':'http://ec2.socialphotos.net:5000/callback_google',
            'grant_type':'authorization_code'
        }
	headers = {'content-type': 'application/x-www-form-urlencoded'}
        url = "https://accounts.google.com/o/oauth2/token"


	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	raw_data = response.read()
	response = json.loads(raw_data)
	access_token=response['access_token']	
	db_util.save_access_token(access_token, 'google_drive', session['email'])
	return redirect('/transfer')

	raw_data = urllib2.urlopen("https://www.googleapis.com/drive/v2/about?access_token=%s" % access_token).read()	
	response = json.loads(raw_data)
	name = response["name"]
	quota_mb = sizeof_fmt(int(response["quotaBytesTotal"]))

	raw_data = urllib2.urlopen("https://www.googleapis.com/drive/v2/files?access_token=%s" % access_token).read()
	response = json.loads(raw_data)
	print response
	return render_template('hello.html',name=name,quota=quota_mb,listFiles=listFiles,response=response)

@app.route('/callback_dropbox')
def callback_dropbox():
	dropbox_token = request.args.get('token','')	
	db_util.save_access_token(dropbox_token, 'dropbox', session['email'])
	return redirect('/transfer')
	print dropbox_token
	raw_data = urllib2.urlopen("https://api.dropbox.com/1/account/info?access_token=%s" % dropbox_token).read()
	data = json.loads(raw_data)
	print data		
	quota=data["quota_info"]["quota"]
	print quota	
	return render_template('dropbox.html',user=data["display_name"], emailId=data["email"], quotaDisplay = sizeof_fmt(int(quota)))

@app.route('/transfer')
def transfer_page():
	return render_template('transfer.html')

@app.route('/transfer_file')
def transfer_file():
	source_drive = get_provider(int(request.args.get('src', '0')))
	destination_drive = get_provider(int(request.args.get('dst', '1')))
	filename = source_drive.download_file(request.args.get('file_id', ''), session['email'])
	destination_drive.upload_file(filename, session['email'])
	return 'okay!'

@app.route('/list_files')
def list_files():
	drive = get_provider(int(request.args.get('drive','0')))
	# check if access token already exists
	if db_util.has_token(session['email'], drive.label):
		files = drive.list_files(session['email'],request.args.get('folder',''))
		return render_template('list_files.html',
								listFiles=files,
								user=session['email'],
								quota='100',
								label=drive.display_label,
								pane=request.args.get('pane','1'),
								drive=request.args.get('drive','0'))
	else:
		print "###", drive.oauth_url
		return render_template('oauth.html',
								label = drive.display_label,
								oauth_url = drive.oauth_url)


def list_files1():
	token = session["token"]
	try:
		folder = request.args.get('folder')
	except KeyError:
		print "no folder variable"

	if(folder == None):
		pass
	else:
		raw_data = urllib2.urlopen("https://apis.live.net/v5.0/%s/files?access_token=%s" % (folder,token)).read()
	
	raw_data1 = urllib2.urlopen("https://apis.live.net/v5.0/me/skydrive/quota?access_token=%s" % token).read()
	quota = json.loads(raw_data1)
	quota_mb = sizeof_fmt(int(quota["available"]))
	#return render_template('page.html',response=response,quota=quota_mb)
	return render_template('list_files.html',listFiles=listFiles,user=response["data"][0]["from"]["name"],quota=quota_mb)

   

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
