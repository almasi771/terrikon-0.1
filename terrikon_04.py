from flask import Flask, render_template, session, request, jsonify, Response, url_for, redirect, flash
from flask.ext.mail import Mail, Message
from werkzeug import secure_filename
from threading import Thread
from collections import defaultdict
from xhtml2pdf import pisa     
from StringIO import StringIO
#from table_fu import TableFu
#import pandas as pd
import os
import csv

#init for uploads
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

mail=Mail(app)

@app.route('/')
@app.route('/index')
def index():
    #return render_template('web_setup.html', available_templates = get_available_templates()    
    return render_template('web_setup.html')


@app.route('/test')
def test():
    return render_template('available_colms.html')

'''
#test for emailing - works correctly
def email_test():
    msg = Message(
           'Hello',
           sender='almasi77@gmail.com',
           recipients=['almasi77@hotmail.com'])
    msg.body = "This is the email body"
    msg.html = "<b> This is the email body </b>"
    mail.send(msg)
    return "Sent"
'''


def fixText(text):
    row = []
    z = text.find(',')
    if z == 0:  
        row.append('')
    else:   
        row.append(text[:z])
    for x in range(len(text)):
        if text[x] != ',':  
            pass
        else:
            if x == (len(text)-1):  
                row.append('')
            else:
                if ',' in text[(x+1):]:
                    y = text.find(',', (x+1))
                    c = text[(x+1):y]
                else:   
                    c = text[(x+1):]
                row.append(c)
    return row
 
def createTuple(oldFile):
    f1 = open(oldFile, "r")
    tup = []
    while 1:
        text = f1.readline()
        if text == "":  
            break
        else:   
            pass
        if text[-1] == '\n':
            text = text[:-1]
        else:   
            pass
        row = fixText(text)
        tup.append(row)
    return tup

#make async later on as it takes too long to load
def send_mail(subject, sender, recipients, txt_body, html_body, attachment,filename):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = txt_body
    msg.html = html_body
    with app.open_resource(attachment) as fp:
        msg.attach(filename, "text/html", fp.read())
    mail.send(msg)

def convertHTMLtoPDF(sourceHtml, outputFilename):
    # open output file for writing (truncated binary)
    resultFile = open(outputFilename, "w+b")

    # convert HTML to PDF
    pisaStatus = pisa.CreatePDF(
            sourceHtml,                # the HTML to convert
            dest=resultFile)           # file handle to recieve result

    # close output file
    resultFile.close()                 # close output file

    return "/Users/administrator/Dropbox/backup/Projects/terrikon_04/"+outputFilename


    """
    pdf = pisa.CreatePDF(
        html_file, 
        file("/Users/administrator/Dropbox/backup/Projects/terrikon_04/uploads/"+filename, "wb"))
    return "/Users/administrator/Dropbox/backup/Projects/terrikon_04/uploads/"+filename
    """

@app.route('/test_email', methods = ['GET', 'POST'])
def test_email():
    #not working because pandas is broken, THANKS MAVERICKS OSX!
    #df_data = pd.read_csv('/Users/almaskebekbayev/Dropbox/backup/Projects/terrikon_04/uploads/terrikon_test_file.csv')
    #emails = parse_data(df_data['Email'])
    
    #read cvs file
    #this needs to be replaced by user's uploaded file
    
    #csv struct - LastName ,Program,DocumentDeadLine,Status,Email
    '''
    cols = defaultdict(list)
    with open('/Users/administrator/Dropbox/backup/Projects/terrikon_04/uploads/terrikon_test_file.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            for (k,v) in row.items():
                cols[k].append(v)
    '''
    f = '/Users/administrator/Dropbox/backup/Projects/terrikon_04/uploads/terrikon_test_file.csv'
    data = createTuple(f)

    if request.method == 'POST':
        #for user_email in cols['Email']:
        for col in data:
            """
            convertHTMLtoPDF(
                render_template('html_email_template.html',
                LastName = str(col[0]),
                Program = str(col[1]),
                DocumentDeadline = str(col[2]),
                Finalist = False,
                Alternate = True),
                str(col[0])+str(col[1])+".pdf")
            """
            send_mail('Terrikon: test email',
                "almasi77@gmail.com",
                [col[4]],
                render_template('sample_email.txt',
                LastName = str(col[0]),
                Program = str(col[1]),
                DocumentDeadline = str(col[2]),
                Finalist = str(col[3]),
                Alternate = str(col[3])),
                render_template('html_email_template.html',
                LastName = str(col[0]),
                Program = str(col[1]),
                DocumentDeadline = str(col[2]),
                Finalist = False,
                Alternate = True), 
                convertHTMLtoPDF(
                    render_template('html_email_template.html',
                    LastName = str(col[0]),
                    Program = str(col[1]),
                    DocumentDeadline = str(col[2]),
                    Finalist = False,
                    Alternate = True),
                    str(col[0])+str(col[1])+".pdf"),
                str(col[0])+str(col[1])+".pdf")
        return redirect(url_for('email_sent'))
        #return str(data)

    return render_template('sample_email.html',
        LastName='Kebekbayev',
        Program = 'FLEX',
        DocumentDeadline = 'Nov. 1, 2013',
        Finalist = False,
        Alternate = True)

@app.route('/email_sent')
def email_sent():
    return render_template('email_sent.html')
	
def allowed_file(filename): 
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/web_setup", methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file and allowed_file(uploaded_file.filename):
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file'))

    #eventially get flash message instead of routes to each html message
    return render_template('upload-error.html')
    #flash(u'Select the file dog')


def get_relative_path_to_templates_dir():
    """
    finds path to templates directory
    """
    for root, dirs, files in os.walk('.'):
        if "templates" in root:
            return root

def get_available_templates():
    """
    returns list of templates that can be used for emails
    """
    result_list = []
    templates_dir = get_relative_path_to_templates_dir()
    for filename in os.listdir(templates_dir):
            result_list.append(filename)
    return result_list

#again pandas extension is not working
'''
def parse_data(series_emails):
    emails = series_emails.tolist()
    return emails
'''

@app.route("/uploaded_file")
def uploaded_file():
	return render_template('file_uploaded.html')

@app.errorhandler(404)
def page_not_found(error):
    return "Dog, what page are you looking for? This one doesn't exist "


#########


if __name__ == "__main__":
    app.run(debug=True)
