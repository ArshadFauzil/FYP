from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP
from io import BytesIO

fr = open('sample.scp', 'r')
fw = open('sample.tok.scp', 'w+')
for line in fr:
    g = tokenize(BytesIO(line.encode('utf-8')).readline)
    tokenized_string = ''
    for five_tuple in g:
        # print(five_tuple.string)
        if (five_tuple.string != 'utf-8'):
            tokenized_string += five_tuple.string+" "
    fw.write(tokenized_string)
    # print(tokenized_string)

fr.close()
fw.close()

# s = "from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP"