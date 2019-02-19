from pprint import pprint

import read_attributes

att = read_attributes.get_only_columns('/media/madusha/DA0838CA0838A781/PC_Interface/Resources/SalesJan2009.csv')

print(att)
my_dict = {}

for a in range(len(att)):
    my_dict['column' + str(a + 1)] = att[a]
    my_dict['attribute' + str(a + 1)] = att[a]
    my_dict['feature' + str(a + 1)] = att[a]
    my_dict[str(a + 1)] = att[a]
    my_dict[att[a]] = att[a]
    my_dict[att[a].lower()] = att[a]
    my_dict[att[a].replace('_', ' ')] = att[a]
    my_dict[att[a].replace(' ', '_')] = att[a]


pprint(my_dict)
