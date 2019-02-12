# from test_spaCy_model import Spacy
import spacy
import csv

UPLOAD_FOLDER = '/media/madusha/DA0838CA0838A781/PC_Interface/Resources/'


class Spacy:
    nlp = spacy.load('en_core_web_lg')
    with open(UPLOAD_FOLDER + 'intents.csv', 'r') as f:
        reader = csv.reader(f)
        intents = list(reader)


c = Spacy()


def find_similar_intent(statement):
    index = 0

    for t in statement:
        max_similarity = 0
        for i in c.intents:
            similarity = c.nlp(t).similarity(c.nlp(i[1]))
            if similarity > max_similarity:
                max_similarity = similarity
                index = int(i[0])

            print(str(similarity) + "\t" + i[1])

        print('Max similarity : ' + c.intents[index][1] + '(' + str(max_similarity) + ')')

        return c.intents[index][1]


if __name__ == '__main__':
    text = ['apply svm', 'repeat until 10']
    find_similar_intent(text)
