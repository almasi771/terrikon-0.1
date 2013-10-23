import os
from table_fu import TableFu
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
 
#Note: change a dir!
UPLOAD_FOLDER = '/Users/administrator/Documents/Projects/terrikon_testing/uploads'
ALLOWED_EXTENSIONS = set(['csv', 'xlsx', 'xls'])
 
app = Flask(__name__)
app.secret_key = "kevinBacon"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename): 
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    #create a template for this + layout for extension
    return render_template('upload_file.html')


if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=5001, debug=True)
    app.run(debug=True)