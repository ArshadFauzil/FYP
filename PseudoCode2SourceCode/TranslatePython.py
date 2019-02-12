import sys
import nltk

arg = sys.argv

with open(arg[1], 'r') as f:
    for line in f:
        tokensl = nltk.word_tokenize(line)
        with open('sample.pcp', 'r') as c:
            for stmt in c:
                tokensc = nltk.word_tokenize(stmt)
                #  MULTILINE TRANSLATION
                if(tokensc[0] == '#' or tokensc[0] == '$'):
                    tokensc.remove(tokensc[0])
                    if(tokensl == tokensc):
                        print(line)
                #  SINGLE LINE TRANSLATION
                else:
                    if(tokensl == tokensc):
                        # CALL THE TRANSLATION MODEL TO TRANSLATE THE CODE LINE
                        print(line)
