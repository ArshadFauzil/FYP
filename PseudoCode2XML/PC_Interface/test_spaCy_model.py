import spacy
import csv

UPLOAD_FOLDER = '/media/madusha/DA0838CA0838A781/PC_Interface/Resources/'


class Spacy:
    nlp = spacy.load('en_core_web_lg')
    with open(UPLOAD_FOLDER + 'intents.csv', 'r') as f:
        reader = csv.reader(f)
        intents = list(reader)



