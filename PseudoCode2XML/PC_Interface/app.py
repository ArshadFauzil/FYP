from __future__ import absolute_import
from pprint import pprint
import os
from flask import Flask, render_template, request, session, abort

app = Flask(__name__)

app.secret_key = "AS9UjjJI0J0JS9j"


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


def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversation."""
    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        print('=' * 20)
        print('Query text: {}'.format(response.query_result.query_text))
        print('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        print('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text))


def test_detect_intent_texts(capsys):
    detect_intent_texts(PROJECT_ID, SESSION_ID, TEXTS, 'en-US')
    out, _ = capsys.readouterr()

    assert 'Fulfillment text: All set!' in out

# [END dialogflow_detect_intent_text]

# @app.route('/detect_intent_texts', methods=['GET', 'POST'])
# def detect_intent_texts(project_id, session_id, text, language_code):
#     session_client = dialogflow.SessionsClient()
#     session = session_client.session_path(project_id, session_id)
#
#     if text:
#         text_input = dialogflow.types.TextInput(
#             text=text, language_code=language_code)
#         query_input = dialogflow.types.QueryInput(text=text_input)
#         response = session_client.detect_intent(
#             session=session, query_input=query_input)
#
#         return response.query_result.fulfillment_text


@app.route('/send_message', methods=['POST'])
def send_message():
    message = "Hi, Name please"
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = {"message": fulfillment_text}
    print(response_text)


@app.route('/')
def home():
    return render_template('wim_phone.html')


@app.route("/find/<string:name>/")
def hello(name):
    return render_template('found_wim_phone.html', name=name)


@app.route('/find_users', methods=['GET'])
def search():
    try:
        phone_price = request.form['price']

        users = findUsersByPrice(phone_price)
        return render_template('found_wim_phone.html', ph_price=phone_price, users_list=users)
    except:
        return render_template('wim_phone.html')


@app.route('/query1', methods=['GET'])
def search1():
    try:
        brand_name = request.form['brandname']
        os = request.form['os']
        phones = recommendPhone(brand_name, os)
        return render_template('result1.html', phone_list=set(phones))
    except:
        return render_template('input_form1.html')


@app.route('/query2', methods=['GET'])
def search2():
    try:
        user_name = request.form['username']
        chipset = request.form['cs']

        phones = RecommendOnChipset(chipset)
        print(phones)
        return render_template('result2.html', name=user_name, phone_cs_list=set(phones))
    except:
        return render_template('input_form2.html')


@app.route('/query3', methods=['GET'])
def search3():
    try:
        user_name = request.form['username']
        agegroup = request.form['age']
        phones = teenPhone(agegroup)
        print(phones)

        return render_template('result3.html', name=user_name, phone_age_list=phones)
    except:
        return render_template('input_form3.html')


@app.route('/query4', methods=['GET'])
def search4():
    try:
        user_name = request.form['username']
        brand_name = request.form['brandname']
        os = request.form['os']

        return render_template('result4.html', name=user_name)
    except:
        return render_template('input_form4.html')


app.add_url_rule('/find_users', 'search', search, methods=['GET', 'POST'])
app.add_url_rule('/query2', 'search2', search2, methods=['GET', 'POST'])
app.add_url_rule('/query3', 'search3', search3, methods=['GET', 'POST'])
app.add_url_rule('/query4', 'search4', search4, methods=['GET', 'POST'])

if __name__ == "__main__":
    app.run(host='localhost', port=3550)
