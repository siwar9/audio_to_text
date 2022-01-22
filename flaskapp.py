from flask import Flask, render_template, url_for, request
from werkzeug.utils import secure_filename
from ibm_watson import SpeechToTextV1, LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os

ltApikey = 'Yl6STe0DkctlW0QhkvAbCvQmpAt58BQwTACQaUxvVe0Z'
ltUrl = 'https://api.eu-gb.language-translator.watson.cloud.ibm.com/instances/886484b9-b63f-4ef2-8555-ea0340459f29'
sttApikey ='Bx2PL46d67eDmpcsBZMojMEf5KBaAjemm-PT-EDgyblO'
sttUrl = 'https://api.eu-de.speech-to-text.watson.cloud.ibm.com/instances/6a93dc79-0194-4758-8ee9-748a2b9d4598'

ltauthenticator = IAMAuthenticator(ltApikey)
lt = LanguageTranslatorV3(version='2018-05-01', authenticator=ltauthenticator)
lt.set_service_url(ltUrl)

sttauthenticator = IAMAuthenticator(sttApikey)
stt = SpeechToTextV1(authenticator=sttauthenticator)
stt.set_service_url(sttUrl)



app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'upload'
app.config['MAX_CONTENT_PATH'] = '3145728'
ALLOWED_EXTENSIONS = {'mp3'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        #googling something rn XD 
        try : 
            if request.files['file'] :
                f = request.files['file']
                    #this is the mp3 file
                if allowed_file(f.filename ):
                    f.save('upload/file.mp3')
                    var = os.listdir('upload')[0]
                    print("******************")
                    print(var)
                    print("******************")
                    #translator code here
                else:
                    return "Wrong file type"

                print("56")
                with open('upload/file.mp3', 'rb') as f:
                    print("58")
                    res = stt.recognize(audio=f, content_type='audio/mp3', model='en-US_NarrowbandModel',).get_result()

                print("59")
                global voicetext 
                voicetext = res['results'][0]['alternatives'][0]['transcript']
                
                

                return render_template('converted.html', convtext = voicetext)
        except:
            pass

    
    arabic='en-ar'
    chinese='en-zh'
    print("63")
    if request.method == 'POST':
            l = request.form.get('language')
            if l.strip() == "Arabic" :
                lang = arabic
            else :
                lang = chinese

            print('================')
            print(l)
            print(lang)
            print('=========')
            translation = lt.translate(text=voicetext, model_id=lang).get_result()
            
            global translatedtext
            translatedtext = translation['translations'][0]['translation']
            print("**********************")
            print(l)
            print(translatedtext)
            print("**********************")

            try:
                if request.form['download']:
                    with open('upload/file.txt', 'w', encoding="utf-8") as f:
                        f.write(translatedtext)
            except:
                pass



            return render_template('converted.html', convtext = translatedtext)
    


if __name__ == '__main__':
    app.run(debug=True)