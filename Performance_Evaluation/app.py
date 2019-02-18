from __future__ import absolute_import
from pprint import pprint
import os
from flask import Flask, render_template, request, session, abort, flash, url_for, send_file
from flask_bootstrap import Bootstrap
import Similarity

def create_app():
  app = Flask(__name__)
  Bootstrap(app)

  return app

app = create_app()

PROJECT_ID = os.getenv('GCLOUD_PROJECT')
SESSION_ID = 'session_pc'
# UPLOAD_FOLDER = '/home/madusha/'
UPLOAD_FOLDER = '/media/madusha/DA0838CA0838A781/PC_Interface/Resources'
ALLOWED_EXTENSIONS = set(['csv', 'txt'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
url_ds_attributes = 'https://api.dialogflow.com/v1/entities/ds_attributes'
url_ds_name = 'https://api.dialogflow.com/v1/entities/Dataset_Name'


@app.route('/payload', methods=['POST'])
def payload():
    if not request.json:
        abort(400)
    if request.json:
        response = request.json
        pprint(response)

    try:
        content = request.json['queryResult']
        print("_" * 20)
        pprint(content)

    except:
        print("JSON not found")

    return 'none'

@app.route('/')
def home():
    libary1 = Similarity.libary1
    libary2 = Similarity.libary2
    line1 = Similarity.line1
    match_df,line2 = Similarity.match()
    return render_template('result3.html', match_df=match_df.to_html(),line1 = line1,line2=line2,libary1=libary1,libary2=libary2)

@app.route('/evl', methods=['GET'])
def evaluate_results():
    match_df = Similarity.match()
    return render_template('result3.html', match_df=match_df.to_html())

@app.route('/match')
def match():
    match_df = Similarity.match()
    return render_template('result3.html', match_df = match_df.to_html())


app.add_url_rule('/match', 'match', match, methods=['GET', 'POST'])


if __name__ == "__main__":
    app.run(host='localhost', port=3550, debug=True)
