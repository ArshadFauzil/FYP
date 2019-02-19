import re
from pprint import pprint
import os
from google.oauth2 import service_account
import test_detect_intent
from entities import create_attribute_dict

credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
credentials = service_account.Credentials.from_service_account_file(credentials_path)
PROJECT_ID = os.getenv('GCLOUD_PROJECT')

# full_corpus = open('/media/madusha/DA0838CA0838A781/PC_Interface/entities/processed_lines.txt')
full_corpus = open('/media/madusha/DA0838CA0838A781/PC_Interface/entities/temp')
lines = [line for line in full_corpus.readlines() if line.strip()]

regex_var = r"\b([Vv]ariable)|([Nn]ame)|([Ll]ist)|([Aa]rray)|\=|([Ii]mport)|([Uu]se)|([Ii]nstance)\b"
regex_num = r"\d+\.?\d*\b"
regex_import = r"\b([Ii]mport)|([Uu]se)|([Ii]nbuilt)|([Ss]uitable)|([Aa]ppropriate)\b"


def generate_entities(extract, req_ent, defined_entities):
    for line in lines:
        print(line)
        intention = test_detect_intent.detect_intent_texts(PROJECT_ID, 'fake', [line], language_code='en')
        print(intention)
        req_ent_int = req_ent[intention]
        print(req_ent_int)
        if 'value' in req_ent_int and 'var_name' in req_ent_int:
            print('pass')
            # entities = list(extract.extract_entities(line))
            # pprint(entities)
            # params = entities_varname_value(entities, req_ent_int)
            # try:
            #     print('var name : {}'.format(params[0]))
            #     print('value : {}'.format(params[1]))
            # except:
            #     print('var_name and value not received')
            print('*' * 40)

        elif 'N' in req_ent_int:
            print('No need of entity')
            print('*' * 40)

        elif 'var_name' in req_ent_int and len(req_ent_int) == 1:
            print('pass')
            # entities = list(extract.extract_entities(line))
            # pprint(entities)
            # param = entities_varname(entities)
            # try:
            #     print('var name : {}'.format(param))
            # except:
            #     print('var_name is not received')
            print('*' * 40)

        elif 'def_value' in req_ent_int and len(req_ent_int) == 1:
            print('pass')
            # entities = list(extract.extract_entities(line))
            # pprint(entities)
            # param = entities_def_value(entities, defined_entities)
            # try:
            #     print('var name : {}'.format(param))
            # except:
            #     print('var_name is not received')
            print('*' * 40)

        elif 'mul_values' in req_ent_int and len(req_ent_int) == 1:
            attributes = create_attribute_dict.create_dict()
            pprint(attributes)
            # entities = list(extract.extract_entities(line))
            # pprint(entities)

            # param = entities_def_value(entities, defined_entities)
            # try:
            #     print('var name : {}'.format(param))
            # except:
            #     print('var_name is not received')
            # print('*' * 40)


def entities_varname_value(entities, required_entities):
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


def entities_varname(entities):
    var_name = ''
    ignore = ['list', 'array', 'memory', 'null', 'empty', 'null array', 'empty array', 'null list', 'empty list']
    for entity in entities:
        if re.search(regex_var, entity) and len(entity.split()) > 1:
            # print('The entity {} contain variable'.format(entity))
            for token in entity.split():
                if not re.search(regex_var, token) and token not in ignore:
                    var_name = token
        elif not re.search(regex_num, entity) and len(entity.split()) == 1 and entity not in ignore:
            var_name = entity

    return var_name


def entities_def_value(entities, def_entities):
    var_name = ''
    for entity in entities:
        entity = entity.replace('=', '').strip()
        if entity in def_entities or entity.lower() in def_entities:
            try:
                var_name = def_entities[entity]
            except:
                var_name = def_entities[entity.lower()]

        elif re.search(regex_import, entity) and len(entity.split()) > 1:
            temp = ''
            for token in entity.split():
                if not re.search(regex_import, token):
                    temp += token + ' '
            print(temp)

            if temp.strip() in def_entities or temp.strip().lower() in def_entities:
                var_name = def_entities[temp.strip()]

    return var_name
