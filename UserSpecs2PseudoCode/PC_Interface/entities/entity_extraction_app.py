# text = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility " \
#        "of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. " \
#        "Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating" \
#        " sets of solutions for all types of systems are given. These criteria and the corresponding algorithms " \
#        "for constructing a minimal supporting set of solutions can be used in solving all the considered types of " \
#        "systems and systems of mixed types."

# pc_lines = get_pseudocode_from_db()[18]
# # print(pc_lines)
# line = 'winning_rate is a double variable which has value 4.00564'
# list1 = list(extract.extract_entities(line))
# pprint(list1)
# print('*' * 20)

full_corpus = open('/media/madusha/DA0838CA0838A781/PC_Interface/entities/processed_lines.txt')
lines = [line for line in full_corpus.readlines() if line.strip()]

entity_map = open('/media/madusha/DA0838CA0838A781/PC_Interface/entities/entity_map').read()
req_ent = {}

for i, line in enumerate(entity_map.split("\n")):
    content = line.split(',')
    try:
        req_ent[content[0]] = (content[1:])
    except:
        print("Unable to locate entity map")

# pprint(req_ent['For each loop'])
extract = Extractor()
regex_var = r"\b([Vv]ariable)|([Nn]ame)|([Ll]ist)|([Aa]rray)|=|([Ii]mport)|([Uu]se\b"
regex_num = r"\d+\.?\d*\b"

for line in lines:
    var_name = ''
    val = ''
    print(line)
    intent = test_detect_intent.detect_intent_texts(PROJECT_ID, 'fake', [line], language_code='en')
    print(intent)
    print(req_ent[intent])
    entities = list(extract.extract_entities(line))
    pprint(entities)

    for rent in req_ent[intent]:
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

    print('var_name :' + var_name)
    print('value :' + val)
    print('*' * 20)