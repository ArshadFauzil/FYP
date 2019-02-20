from __future__ import absolute_import
from flask import Flask, render_template, request, session, abort, flash, url_for, send_file
from flask_bootstrap import Bootstrap
import Similarity

def create_app():
  app = Flask(__name__)
  Bootstrap(app)
  return app

app = create_app()

@app.route('/', methods=['GET'])
def home():
    match_df,line1,line2,libaryName1,libaryName2,RalgoArr,SKalgoArr = Similarity.match()
    RalgoArr = list(RalgoArr["algorithm"].values)
    SKalgoArr = list(SKalgoArr["algorithm"].values)
    return render_template('result3.html', match_df=match_df.to_html(),line1 = line1,line2=line2,libaryName1=libaryName1,libaryName2=libaryName2,RalgoArr=RalgoArr,SKalgoArr=SKalgoArr,algoName1=Similarity.algoName1,algoName2=Similarity.algoName2,lang1=Similarity.lang1,lang2=Similarity.lang2)

@app.route('/evl', methods=['GET'])
def evaluate_results():
    Similarity.algoName1 = request.form['select1']
    Similarity.algoName2 = request.form['select2']
    Similarity.lang1 = request.form['selectLan1']
    Similarity.lang2 = request.form['selectLan2']
    match_df,line1,line2,libaryName1,libaryName2,RalgoArr,SKalgoArr = Similarity.match()
    RalgoArr = list(RalgoArr["algorithm"].values)
    SKalgoArr = list(SKalgoArr["algorithm"].values)
    return render_template('result3.html', match_df=match_df.to_html(),line1 = line1,line2=line2,libaryName1=libaryName1,libaryName2=libaryName2,RalgoArr=RalgoArr,SKalgoArr=SKalgoArr,algoName1=Similarity.algoName1,algoName2=Similarity.algoName2,lang1=Similarity.lang1,lang2=Similarity.lang2)

app.add_url_rule('/evl', 'evl', evaluate_results, methods=['GET', 'POST'])

if __name__ == "__main__":
    app.run(host='localhost', port=3550, debug=True)
