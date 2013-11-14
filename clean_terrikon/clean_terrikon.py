from flask import Flask, render_template, session, request, jsonify, Response, url_for, redirect, flash
from flask.ext.mail import Mail, Message
from werkzeug import secure_filename
from threading import Thread
from collections import defaultdict
from xhtml2pdf import pisa     
from StringIO import StringIO
import os
import csv

#NOTE: CHANGE THE PATH to /path/to/up
UPLOAD_FOLDER = '/Users/administrator/Documents/Projects/terrikon_04/uploads'
ALLOWED_EXTENSIONS = set(['csv', 'xlsx', 'xls'])

app = Flask(__name__)
mail = Mail(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#max uploaded file is 16 MB
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024

#EMAIL SETTINGS
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_SSL= False,
    MAIL_USE_TLS = True,
    MAIL_USERNAME = 'almasi77@gmail.com', 
    MAIL_PASSWORD = 'caLAk7y7' #REMOVE BEFORE GIT
    )

def main():
	print 'well hello clean terrikon'

if __name__ == '__main__':
	main()