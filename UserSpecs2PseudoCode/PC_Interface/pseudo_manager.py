from pprint import pprint

import re

from entities import entity_extraction_app


def get_response(response, pseudo_gen):
    parm_map = pseudo_gen.parm_map
    idnt_map = pseudo_gen.idnt_map
    query_text = response.query_result.query_text
    intent = response.query_result.intent.display_name
    confidence = response.query_result.intent_detection_confidence
    fulfillment = response.query_result.fulfillment_text
    parameters = dict(response.query_result.parameters)

    print('Query text: {}'.format(query_text))
    print('Detected intent: {} (confidence: {})\n'.format(intent, confidence))
    print('Fulfillment text: {}\n'.format(fulfillment))
    print(parameters)
    wc = pseudo_gen.wildcard

    if idnt_map[intent] == 'N':
        print('No entities involved')
    elif idnt_map[intent] == 'DF':
        print('Entities handle by DF')
    elif idnt_map[intent] == 'ER':
        print('Entities handle by ER')
        process_er(query_text, intent, parameters, pseudo_gen, wc)

    print(wc)


def process_er(query, intent, parameters, pseudo_gen, wild_cd):
    extract = pseudo_gen.extract
    entities_from_er = entity_extraction_app.generate_entities(extract, intent, query)
    
    if intent == 'Assign value to float variable' or intent == 'Assign value to integer variable':
        var_name = 'VAR' + str(len(pseudo_gen.varn))
        var_val = 'VAR_VALUE' + str(len(pseudo_gen.var_value))
        pseudo_gen.varn.append(var_name)
        pseudo_gen.var_value.append(var_val)
        wild_cd[var_name] = entities_from_er[0]
        wild_cd[var_val] = entities_from_er[1]

        replacements = {'VAR': var_name, 'VAR_VALUE': var_val}

        def replace(match):
            return replacements[match.group(0)]

        print(re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in replacements), replace, 'define variable VAR and '
                                                                                        'assign VAR_VALUE'))



    # if intent == 'Append elements to a list':
    #     standard_pc = 'define array STRING_ARRAY with values STRING_VALUES'
    #
    #     for r in (("STRING_ARRAY", "red"), ("STRING_VALUES", "quick")):
    #         standard_pc = standard_pc.replace(*r)

    # len_param = len(parameters)
    # print(len_param)
    #
    # if len_param == 1:
    #     entities_from_er = entity_extraction_app.generate_entities(extract, intent, query_text)
    #     try:
    #         print(list(parameters.keys())[0] + ":" + entities_from_er[0])
    #     except:
    #         print(list(parameters.keys())[0] + ":" + str(len(entities_from_er[0])))
    #
    # if len_param > 1:
    #     entities_from_er = entity_extraction_app.generate_entities(extract, intent, query_text)
    #     entity_name = list(parameters.keys())
    #     for en in entity_name:
    #         try:
    #             er_name = parm_map[en]
    #         except:
    #             er_name = 'None'
    #         if er_name == 'var_name':
    #             print(en + ":" + entities_from_er[0])
    #         elif er_name == 'percentage':
    #             print(en + ":" + entities_from_er[0])
    #         elif er_name is not 'none':
    #             print(en + ":" + entities_from_er[1])
