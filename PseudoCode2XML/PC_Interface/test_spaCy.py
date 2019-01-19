# import spacy
# nlp = spacy.load('en')
# doc = nlp('Hello     World!')
# for token in doc:
#     print('"' + token.text + '"', token.idx)

import spacy

nlp = spacy.load('en_core_web_lg')
nlp_en = spacy.load('en')

intents = ['requesting accuracy',
           'K is integer $number',
           'classify data frame using Algorithm',
           'define target class',
           'import Data Manipulation Library',
           'import multidimensional array operator',
           'drop attributes',
           'terminate classification',
           'use programming language',
           'read csv file',
           'import machine learning library',
           'test ratio is',
           'train ratio is',
           'create model',
           'apply cross validation',
           'delete model'
           ]

max_similarity = 0
index = 0
max_index = 0

for s in intents:
    similarity = nlp('apply svm').similarity(nlp(s))
    if similarity > max_similarity:
        max_similarity = similarity
        max_index = index

    index += 1
    print(similarity)

print('Max similarity : ' + intents[max_index] + '(' + str(max_similarity) + ')')
