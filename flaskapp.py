from flask import Flask, render_template, url_for, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'upload'
app.config['MAX_CONTENT_PATH'] = '3145728'


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      sf = f.save(secure_filename(f.filename))   #this is the mp3 file

      #translator code here
      

      return render_template('converted.html')

if __name__ == '__main__':
    app.run(debug=True)