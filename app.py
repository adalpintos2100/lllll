import requests,json,urllib.parse,time
import shutil
from flask_cors import CORS
from flask import Flask, request, render_template

def recaptcha(url):
    q = requests.get(url, stream=True)
    with open('audio.mp3', 'wb') as f:
        shutil.copyfileobj(q.raw, f)
    r = json.loads(requests.post("http://ct1.ofoct.com/upload.php", files={'myfile': open('audio.mp3', 'rb')}).text)
    req = requests.get('http://ct1.ofoct.com/convert-file_v2.php?cid=audio2txt&output=txt&tmpfpath='+r[0]+'&sourcename=audio.mp3&sdk=baidu')
    result = requests.get('http://ct1.ofoct.com/get-file.php?type=get&genfpath='+req.text.split("|")[2]+'&downloadsavename=audio.mp3.txt').text
    return result

app = Flask(__name__) #create the Flask app
CORS(app)
@app.route('/sms')
def result():
    return 'hola'
@app.route('/data')
def data():
    return recaptcha(urllib.parse.unquote(request.args['audio'])).replace(",", "")
if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD']=True
    app.run(port=5000,debug=True,use_reloader=True)
