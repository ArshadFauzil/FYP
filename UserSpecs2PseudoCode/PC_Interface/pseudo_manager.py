from pprint import pprint

from entities import entity_extraction_app


def get_response(response, pseudo_gen):
    extract = pseudo_gen.extract
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
        wc['DATASET'] = 'csv'
        print(wc)
    elif idnt_map[intent] == 'DF':
        print('Entities handle by DF')
    elif idnt_map[intent] == 'ER':
        print('Entities handle by ER')
        wc['NEIGHBORS'] = 10
        print(wc)


def process_er(query, intent, parameters, extract):
    st_array, st_values, varn, var_value = []
    entities_from_er = entity_extraction_app.generate_entities(extract, intent, query)



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
