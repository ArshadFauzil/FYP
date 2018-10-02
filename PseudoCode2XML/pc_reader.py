import os
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

# from nltk.tokenize import sent_tokenize

root_path = os.path.normpath(os.getcwd() + os.sep + os.pardir) + '/PC2SC/Resources'
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


for line in lines:
    print(line)
    tkns_in_line = tokenize_text(line)
    print(tkns_in_line)
    tkn_with_postag = pos_tag(tkns_in_line)
    lmtzd_tkns_in_line = lemmatize_tokens(tkns_in_line)
    print(tkn_with_postag)
    print(tkn_with_postag[1])

print(len(lines))
