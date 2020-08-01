from datetime import datetime
from flask import Flask, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'secret_key'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Not an image')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            os.system("rm ./uploads/*")
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            now = datetime.now()
            time_id = '{:02d}'.format(now.day)+"-"+'{:02d}'.format(now.month)+"-"+str(now.year)+"-"+'{:02d}'.format(now.hour-3)+":"+'{:02d}'.format(now.minute)+":"+'{:02d}'.format(now.second)
            f = open('./report.txt', 'a')
            f.write(str(time_id)+ " " +filename + '\n')
            f.close()
            os.system('python3 face.py ' + filepath)
            
        return redirect(url_for('uploaded_file', filename='out'+filename))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
