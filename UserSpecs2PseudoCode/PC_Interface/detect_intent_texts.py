import os
from google.oauth2 import service_account
from pseudo_manager import get_response
from Similarity_engine import find_similar_intent
from entities import entity_extractor

credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
credentials = service_account.Credentials.from_service_account_file(credentials_path)
PROJECT_ID = os.getenv('GCLOUD_PROJECT')

print('Credendtials from environ: {}'.format(credentials))


class PseudoGen:
    extract = entity_extractor.Extractor()
    df_entity = open('/media/madusha/DA0838CA0838A781/PC_Interface/Resources/df_entity').read()
    parm_map = {}

    for i, line in enumerate(df_entity.split("\n")):
        try:
            if line is not '':
                content = line.split(',')
            parm_map[content[0]] = (content[1])
        except:
            print("Unable to locate df_entity map")


pg = PseudoGen()


def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversation."""
    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient(credentials=credentials)

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    query_text = response.query_result.query_text
    intent = response.query_result.intent.display_name
    confidence = response.query_result.intent_detection_confidence
    fulfillment = response.query_result.fulfillment_text
    parameters = response.query_result.parameters

    print('=' * 40)
    # print('Query text: {}'.format(query_text))
    # print('Detected intent: {} (confidence: {})\n'.format(intent, confidence))
    # print('Fulfillment text: {}\n'.format(fulfillment))
    # print('Parameter Entity : {}'.format(parameters))

    if fulfillment == 'unknown':
        fulfillment = find_similar_intent(str(query_text))
        print('Fulfillment text (by SE): {} (similarity: {})\n'.format(fulfillment[0], fulfillment[1]))

    get_response(response, pg)
    return fulfillment


if __name__ == '__main__':
    # lines = ['find confusion matrix', 'obtain the predicted classes for my_list by using the model', 'assign 6 to variable rt']
    full_corpus = open('/media/madusha/DA0838CA0838A781/PC_Interface/entities/testing')
    lines = [line for line in full_corpus.readlines() if line.strip()]

    for line in lines:
        detect_intent_texts(PROJECT_ID, 'df', line, language_code='en')
