import re
from pprint import pprint
import os
from google.oauth2 import service_account
import test_detect_intent

credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
credentials = service_account.Credentials.from_service_account_file(credentials_path)
PROJECT_ID = os.getenv('GCLOUD_PROJECT')

full_corpus = open('/media/madusha/DA0838CA0838A781/PC_Interface/entities/processed_lines.txt')
lines = [line for line in full_corpus.readlines() if line.strip()]

regex_var = r"\b([Vv]ariable)|([Nn]ame)|([Ll]ist)|([Aa]rray)|\=|([Ii]mport)|([Uu]se)|([Ii]nstance)\b"
regex_num = r"\d+\.?\d*\b"


def generate_entities(extract, req_ent):
    for line in lines:
        print(line)
        intention = test_detect_intent.detect_intent_texts(PROJECT_ID, 'fake', [line], language_code='en')
        print(intention)
        req_ent_int = req_ent[intention]
        print(req_ent_int)
        if 'value' in req_ent_int and 'var_name' in req_ent_int:
            entities = list(extract.extract_entities(line))
            pprint(entities)
            params = entities_for_varname_value(entities, req_ent_int)
        # entities = list(extract.extract_entities(line))
        # pprint(entities)
        try:
            print('var name : {}'.format(params[0]))
            print('value : {}'.format(params[1]))
        except:
            print('var_name and value not received')


def entities_for_varname_value(entities, required_entities):
    var_name = ''
    val = ''
    for rent in required_entities:
        if rent == 'var_name':
            for entity in entities:
                if re.search(regex_var, entity):
                    # print('The entity {} contain variable'.format(entity))
                    for token in entity.split():
                        if not re.search(regex_var, token):
                            var_name = token
                elif not re.search(regex_num, entity):
                    var_name = entity

        elif rent == 'value':
            for entity in entities:
                if re.search(regex_num, entity):
                    # print('The entity {} contain number'.format(entity))
                    e = entity.replace(',', '')
                    val = e

    return [var_name, val]

