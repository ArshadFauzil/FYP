import re

regex_var = r"\b[Vv]ariable\b"
regex_num = r"\d+\.?\d*\b"
text = 'define an integer Vvariable named kegalle and assign 849892'
entities = ['integer variable x', '849,892.056']
matches = re.search(regex_var, text)

var_name = ''
val = ''
for entity in entities:
    if re.search(regex_var, entity):
        print('The entity {} contain variable'.format(entity))
        for token in entity.split():
            if not re.search(regex_var, token):
                var_name = token

    elif re.search(regex_num, entity):
        print('The entity {} contain number'.format(entity))
        e = entity.replace(',', '')
        val = e

    else:
        print('No variable name and value')

print('var_name :' + var_name)
print('value :' + val)
