#!/usr/bin/python

# A python script connecting to a MongoDB given a MongoDB Connection URI.

import sys
import pymongo
import hashlib

### Standard URI format: mongodb://[dbuser:dbpassword@]host:port/dbname
client = None

def db_open():
	global client
	MONGODB_URI = 'mongodb://synergy:synergy@ds049558.mongolab.com:49558/synergy' 
	client = pymongo.MongoClient(MONGODB_URI)
	db = client.get_default_database()
	return db['users']	

def db_close():
	global client
	client.close()

def user_signup(email,password):
	users = db_open()
	query = users.find_one({'email': email})
	if(query == None):
		users.insert({ "email": email ,"password" : password })
	else:
		print "Record with Email ID Already present (%s) "% (query["email"])
	db_close()

def save_access_token(token,label,email):
	users = db_open()
	query = users.find_one({'email': email})
	query[label] = token
	users.save(query)
	db_close()

def fetch_access_token(email,label):
	users = db_open()
	query = users.find_one({'email': email})
	db_close()
	return query.get(label,None)

def has_token(email, label):
	return fetch_access_token(email, label) != None

if __name__ == '__main__':
    main(sys.argv[1:])
