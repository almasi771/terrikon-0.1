from flask import Flask, render_template, session, request, jsonify, Response, url_for, redirect, flash
from flask.ext.mail import Mail, Message
from werkzeug import secure_filename
from threading import Thread
from table_fu import TableFu
import os

#init for uploads
UPLOAD_FOLDER = '/Users/administrator/Documents/Projects/terrikon_04/uploads'
ALLOWED_EXTENSIONS = set(['csv', 'xlsx', 'xls'])

app = Flask(__name__)
mail = Mail(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#EMAIL SETTINGS
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_SSL= False,
    MAIL_USE_TLS = True,
    MAIL_USERNAME = 'almasi77@gmail.com', 
    MAIL_PASSWORD = '######' #REMOVE BEFORE GIT
    )

mail=Mail(app)

@app.route('/')
@app.route('/index')
def index():
    #return render_template('web_setup.html', available_templates = get_available_templates()    
    return render_template('web_setup.html')
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

#make async later on as it takes too long to load
def send_mail(subject, sender, recipients, txt_body, html_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = txt_body
    msg.html = html_body
    mail.send(msg)

@app.route('/test_email', methods = ['GET', 'POST'])
def test_email():
    if request.method == 'POST':
        send_mail('Terrikon: test email',
            "almasi77@gmail.com",
            ['almasi77@hotmail.com'],
            render_template('sample_email.txt',
                LastName = 'Kebekbayev',
                Program = 'FLEX',
                DocumentDeadline = 'Nov. 1, 2013',
                Finalist = True,
                Alternate = False),
            render_template('html_email_template.html',
                LastName = 'Kebekbayev',
                Program = 'FLEX',
                DocumentDeadline = 'Nov. 1, 2013',
                Finalist = True,
                Alternate = False))
        return redirect(url_for('email_sent'))
    
    return render_template('sample_email.html',
        LastName='Kebekbayev',
        Program = 'FLEX',
        DocumentDeadline = 'Nov. 1, 2013',
        Finalist = True,
        Alternate = False)

@app.route('/email_sent')
def email_sent():
    return render_template('email_sent.html')
	
def allowed_file(filename): 
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/web_setup", methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
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

@app.route("/uploaded_file")
def uploaded_file():
	return render_template('file_uploaded.html')

@app.errorhandler(404)
def page_not_found(error):
    return "Dog, what page are you looking for? This one doesn't exist "

if __name__ == "__main__":
    app.run(debug=True)
