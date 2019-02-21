from entities import entity_extractor, entity_extraction_app

extract = entity_extractor.Extractor()


def get_response(response):
    query_text = response.query_result.query_text
    intent = response.query_result.intent.display_name
    confidence = response.query_result.intent_detection_confidence
    fulfillment = response.query_result.fulfillment_text
    parameters = dict(response.query_result.parameters)

    print('Query text: {}'.format(query_text))
    print('Detected intent: {} (confidence: {})\n'.format(intent, confidence))
    print('Fulfillment text: {}\n'.format(fulfillment))
    print(parameters)
    len_param = len(parameters)
    print(len_param)

    if len_param == 1:
        entities_from_ER = entity_extraction_app.generate_entities(extract, intent, query_text)
        print(entities_from_ER)
