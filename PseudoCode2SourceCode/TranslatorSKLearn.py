import xml.etree.ElementTree as ET
from nltk import CFG, RegexpTagger
import re

def hasLabel(parent, tchild):
    for child in parent:
        if child.tag == tchild:
            return True
    return False



# MAKE THE NESTED CHILDREN TRAVERSAL DYNAMIC FOR DEPTH > 2

def verifygrammar(label, codestring, varname):
    regexp_tagger = RegexpTagger(
        [
            (r"^[0-9]+$", "decimal"),
            (r"^0x[0-9A-Fa-f]+$", "hexadecimal"),
        ])
    # VARIABLE LINE GENERATION - Assumption - Complex numbers data types are ignored for data mining algorithms
    if label.tag == 'var':
        varGrammar = CFG.fromstring("""
            S -> VN "=" VV
            VN -> """+varname+"""
            VV -> I | D | ST | B
            B -> True | False
            I -> I N | N
            D -> I"."F
            F -> F N | N
            ST -> "'"STI"'"
            STI -> S N | S C | N | C
            N -> 0|1|2|3|4|5|6|7|8|9
            C -> a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z
            """)
    elif label.tag == 'array':
        arrayGrammar = CFG.fromstring("""
            S -> AN "= [" AE "]"
            AN -> """ + varname + """
            AE -> VV AE | VV
            VV -> I | D | ST | B
            B -> True | False
            I -> I N | N
            D -> I"."F
            F -> F N | N
            ST -> "'"STI"'"
            STI -> S N | S C | N | C
            N -> 0|1|2|3|4|5|6|7|8|9
            C -> a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z
            """)

def translate(label):
    codestring = ''
    # VARIABLE LINE GENERATION
    if label.tag == 'var':
        if hasLabel(label, 'value'):
            codestring += label[0].text+" = "+label[2].text
        else:
            if label[1].text == 'double':
                codestring += label[0].text+" = 0.0"
            elif label[1].text == 'string':
                codestring += label[0].text + " = ''"
            elif label[1].text == 'integer':
                codestring += label[0].text + " = 0"
            elif label[1].text == 'boolean':
                codestring += label[0].text + " = False"
        return codestring
    # ARRAY LINE GENERATION
    elif label.tag == 'array':
        if hasLabel(label, 'values'):
            codestring += label[0].text + " = ["
            for value in label[2]:
                codestring += value.text + ","
            codestring += "]"
        else:
            codestring += label[0].text + " = []"
        return codestring
    # WHILE LOOP GENERATION
    elif label.tag == 'while':
        loopcondition = label.text


root = ET.parse('sample.xml').getroot()
a = ''
# print(root.tag)

for child in root:
    if child.tag == 'var' or child.tag == 'array':
        print(translate(child))

filestring = 'import numpy as np\nimport pandas as pd\nfrom sklearn import preprocessing, model_selection, neighbors, svm'

