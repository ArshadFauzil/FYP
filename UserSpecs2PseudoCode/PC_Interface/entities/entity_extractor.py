import difflib
import re
from nltk import RegexpParser
from entities import entity_extraction_app
from stanford_pos_tagger.stanfordapi import StanfordAPI
from pprint import pprint
import os
import pymongo
import test_detect_intent
from google.oauth2 import service_account

credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
credentials = service_account.Credentials.from_service_account_file(credentials_path)
PROJECT_ID = os.getenv('GCLOUD_PROJECT')

myclient = pymongo.MongoClient(os.getenv('MONGO_CLIENT'))
pc_db = myclient[os.getenv('MONGO_DB')]


class Extractor:
    pos_tag_obj = StanfordAPI()

    entity_map = open('/media/madusha/DA0838CA0838A781/PC_Interface/entities/entity_map').read()
    req_ent = {}

    for i, line in enumerate(entity_map.split("\n")):
        content = line.split(',')
        try:
            req_ent[content[0]] = (content[1:])
        except:
            print("Unable to locate entity map")

    """Used to extract entities based on POS tagging"""

    # def __init__(self):
    #     self.pos_tag_obj = StanfordAPI()

    @staticmethod
    def tokenize_words(sentence, preserve_case=True):
        """Word separation in a sentence"""
        words = []
        for word in re.split(r'^[-,.()!:+?\"\'*]+|[-,.()!:+?\"\'*]*\s+[-,.()!:+?\"\'*]*|[-,.()!:+?\"\'*]+$', sentence):
            if word != "":
                words.append(word)

        if not preserve_case:
            words = list(map((lambda x: x.lower()), words))
        return words

    @staticmethod
    def sentence_phrases_separation(text):
        """Used for part of sentence extraction based on punctuation delimiters.
        An additional space is added in between period and capital letter"""
        sentence_phrases = [sent for sent in
                            re.split(r'[.,!:;?*()\n]+\s+|\s+[.,!:;?*()\n]+|(->)',
                                     re.sub(r'(\.)([A-Z])', r'\1 \2', text))
                            if
                            sent != '']
        return sentence_phrases

    @staticmethod
    def word_combination(pos_tagged_sentence, tag_set='ptb'):
        """Chunking of a part of speech tagged sentence based on specific grammar"""
        # grammar = r"""
        # EN:{(<JJ>*<NN.*>+<IN>)?<JJ>*<NN.*>+}
        # """
        if tag_set == 'ptb':
            # Entity grammar used for the Penn Tree Bank Tagset
            grammar = r"""
            EN: {<JJ.*>*<NN.*>+|<CD>}
            """
        elif tag_set == 'universal':
            # Entity grammar used for the Universal Tagset
            grammar = r"""
            EN: {<ADJ>*<NOUN>+}
            """
        else:
            raise SyntaxError

        cp = RegexpParser(grammar)
        result = cp.parse(pos_tagged_sentence)
        return result

    @staticmethod
    def calculate_symbol_ratio(word):
        """Calculating the symbol ratio of an element"""
        symbol_ratio = float(len(re.findall(r'[^A-Za-z\s]', word))) / len(word)
        return symbol_ratio

    @staticmethod
    def entity_generation(pos_tagged_tree):
        """Used for the entity generation using the chunked entity tree
        :type pos_tagged_tree: Tree
        """
        # Considering entities in the sentence
        sent_entities = []
        # This list should be given in simple case.
        unimp_tokens = ['stop', 'end']
        ignorable = ['class', 'value', 'values', 'set', 'classes', 'attributes', 'int', 'integer', 'Integer variable', 'float',
                     'floating point', 'double', 'validation', 'return', 'show', 'null variable', 'floating point array', 'array']

        # Traversing through the tree
        whole_entity = []
        neglect = False
        for result_tree in pos_tagged_tree:
            if type(result_tree) is not tuple:
                entity = []
                for subtree in result_tree:
                    # Neglecting the whole sentence if there's a word in the unimp_tokens list
                    if subtree[0].lower() in unimp_tokens:
                        neglect = True

                    # Not appending the words in the ignorable list to the entity list and the word should have at
                    # least more than one character
                    elif subtree[0].lower() not in ignorable:
                        entity.append(subtree[0])

                if entity and not neglect:
                    concat_word = ' '.join([word for word in entity if word])
                    whole_entity.append(concat_word)

        for en in whole_entity:
            sent_entities.append(en)

        for element in sent_entities:
            if element:
                yield element

    def extract_entities(self, text):
        """Used to extract entities based on part of speech tagging
        :type text: str
        """
        # regex = r"\d+\.?\d*\b"
        # matches = re.findall(regex, text)

        input_sentences = self.sentence_phrases_separation(text)
        entities = []
        # entities = [matches]
        for sentence in input_sentences:

            # If sentence is not None
            if sentence:
                tokens = self.tokenize_words(sentence)
                # POS tagging using the Stanford POS tagger
                pos_tagged_sentence = self.pos_tag_obj.pos_tag(' '.join(tokens))
                # print(pos_tagged_sentence)
                result = self.word_combination(pos_tagged_sentence)
                entities += [en for en in list(self.entity_generation(result))]
        return iter(entities)


def comparator(entity_list1, entity_list2, threshold=0.99):
    """Return the equal entities between two entity lists based on it's similarity up to a certain threshold value"""
    equal_entities = []
    for entity1 in entity_list1:
        for entity2 in entity_list2:
            seq = difflib.SequenceMatcher(a=str(entity1).lower(), b=str(entity2).lower())
            if seq.ratio() > threshold:
                equal_entities.append(entity2)
    # return len(set(equal_entities))
    return set(equal_entities)


def get_pseudocode_from_db():
    coll_name = pc_db["pseudocodes"]
    records = list(coll_name.find({}))
    lines = []
    for x in records:
        lines.append(x['PseudoCode'])

    return lines


# def extractor_app():
#     extract = Extractor()


if __name__ == "__main__":
    # pc_lines = get_pseudocode_from_db()[18]
    # # print(pc_lines)
    # line = 'winning_rate is a double variable which has value 4.00564'
    # list1 = list(extract.extract_entities(line))
    # pprint(list1)
    # print('*' * 20)

    extract = Extractor()
    entity_extraction_app.generate_entities(extract, extract.req_ent)

    # full_corpus = open('/media/madusha/DA0838CA0838A781/PC_Interface/entities/processed_lines.txt')
    # lines = [line for line in full_corpus.readlines() if line.strip()]
    #
    # entity_map = open('/media/madusha/DA0838CA0838A781/PC_Interface/entities/entity_map').read()
    # req_ent = {}
    # #
    # for i, line in enumerate(entity_map.split("\n")):
    #     content = line.split(',')
    #     try:
    #         req_ent[content[0]] = (content[1:])
    #     except:
    #         print("Unable to locate entity map")
    #
    # pprint(req_ent['IF condition - not'])
    # extract = Extractor()
    # regex_var = r"\b([Vv]ariable)|([Nn]ame)|([Ll]ist)|([Aa]rray)|=|([Ii]mport)|([Uu]se\b"
    # regex_num = r"\d+\.?\d*\b"
    #
    # for line in lines:
    #     var_name = ''
    #     val = ''
    #     print(line)
    #     intent = test_detect_intent.detect_intent_texts(PROJECT_ID, 'fake', [line], language_code='en')
    #     print(intent)
    #     print(req_ent[intent])
    #     entities = list(extract.extract_entities(line))
    #     pprint(entities)
    #
    #     for rent in req_ent[intent]:
    #         if rent == 'var_name':
    #             for entity in entities:
    #                 if re.search(regex_var, entity):
    #                     # print('The entity {} contain variable'.format(entity))
    #                     for token in entity.split():
    #                         if not re.search(regex_var, token):
    #                             var_name = token
    #                 elif not re.search(regex_num, entity):
    #                     var_name = entity
    #
    #         elif rent == 'value':
    #             for entity in entities:
    #                 if re.search(regex_num, entity):
    #                     # print('The entity {} contain number'.format(entity))
    #                     e = entity.replace(',', '')
    #                     val = e
    #
    #     print('var_name :' + var_name)
    #     print('value :' + val)
    #     print('*' * 20)
