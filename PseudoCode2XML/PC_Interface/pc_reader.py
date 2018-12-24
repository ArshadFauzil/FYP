import os
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
# from nltk.tokenize import sent_tokenize
from detect_intent_texts import detect_intent_texts
import os


PROJECT_ID = os.getenv('GCLOUD_PROJECT')
SESSION_ID = 'fake_session_for_testing'

root_path = os.path.normpath(os.getcwd() + os.sep + os.pardir) + '/PC_Interface/Resources'
os.chdir(root_path)

tokenizer = RegexpTokenizer('\s+', gaps=True)
lemmatizer = WordNetLemmatizer()

pc_file = open('pc1', "r")
pc_read = pc_file.read()

lines = pc_read.split('\n')


# lines = sent_tokenize(pc_read, language='english')

def tokenize_text(c_line):
    tknzd_line = tokenizer.tokenize(c_line)
    tokens = [token.lower() for token in tknzd_line]
    return tokens


def lemmatize_tokens(tokens):
    l_tokens = list(())
    for tks in tokens:
        lemma = lemmatizer.lemmatize(tks, pos="v")
        l_tokens.append(lemma)
    return l_tokens

#
# for line in lines:
#     print(line)
#     tkns_in_line = tokenize_text(line)
#     print(tkns_in_line)
#     lmtzd_tkns_in_line = lemmatize_tokens(tkns_in_line)
#     tkn_with_postag1 = pos_tag(tkns_in_line)
#     tkn_with_postag = pos_tag(lmtzd_tkns_in_line)
#
#     # tt = [lemmatizer.lemmatize(i, j[0].lower()) if j[0].lower() in ['a', 'n', 'v'] else lemmatizer.lemmatize(i) for i, j
#     #       in
#     #       pos_tag(tkns_in_line)]
#
#     print(lmtzd_tkns_in_line)
#     print(tkn_with_postag1)
#     print(tkn_with_postag)

# TEXTS = ["hello", "book a meeting room", "Mountain View",
#          "tomorrow", "10 AM", "2 hours", "10 people", "A", "name please"]

# print(len(lines))

lines = list(filter(None, lines))
print(lines)

def test_detect_intent_texts():
    detect_intent_texts(PROJECT_ID, SESSION_ID, lines, 'en-US')


if __name__ == '__main__':
    test_detect_intent_texts()






