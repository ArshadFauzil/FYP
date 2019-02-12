import nltk
nltk.download('punkt')


fr = open('sample.scr', 'r')
fw = open('sample.tok.scr', 'w+')
pattern = r'''<-|\w+|\(|\)|=|,|\'\w+.\w+\''''
for line in fr:
    g = nltk.regexp_tokenize(line, pattern)
    tokenized_string = ''
    for five_tuple in g:
        # print(five_tuple.string)
        if (five_tuple.string != 'utf-8'):
            tokenized_string += five_tuple.string+" "
    fw.write(tokenized_string)
    # print(tokenized_string)

fr.close()
fw.close()


# # fr = open('sample.scr', 'r')
# # fw = open('sample.tok.scr', 'w+')
# testString = "df <- read_delim(file = 'dataset.txt', delim = ' ' , col_names = TRUE)"
# pattern = r'''<-|\w+|\(|\)|=|,|\'\w+.\w+\''''
#
# tokens = nltk.regexp_tokenize(testString, pattern)
#
# print(tokens)