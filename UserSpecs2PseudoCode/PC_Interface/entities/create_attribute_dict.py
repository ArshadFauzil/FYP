from pprint import pprint
import read_attributes
from collections import defaultdict

data_dict = defaultdict(list)

def create_dict():
    att = read_attributes.get_only_columns('/media/madusha/DA0838CA0838A781/PC_Interface/Resources/SalesJan2009.csv')

    att_dict = {}

    for a in range(len(att)):
        att_dict['column' + str(a + 1)] = att[a]
        att_dict['attribute' + str(a + 1)] = att[a]
        att_dict['feature' + str(a + 1)] = att[a]
        att_dict[str(a + 1)] = att[a]
        att_dict[att[a]] = att[a]
        att_dict[att[a].lower()] = att[a]
        att_dict[att[a].replace('_', ' ')] = att[a]
        att_dict[att[a].replace(' ', '_')] = att[a]

    # pprint(att_dict)
    return att_dict


def create_indexed_dict():
    att = read_attributes.get_only_columns('/media/madusha/DA0838CA0838A781/PC_Interface/Resources/SalesJan2009.csv')

    att_dict = {}

    for a in range(len(att)):
        att_dict['column' + str(a + 1)] = a+1
        att_dict['attribute' + str(a + 1)] = a+1
        att_dict['feature' + str(a + 1)] = a+1
        att_dict[str(a + 1)] = a+1
        att_dict[att[a]] = a+1
        att_dict[att[a].lower()] = a+1
        att_dict[att[a].replace('_', ' ')] = a+1
        att_dict[att[a].replace(' ', '_')] = a+1
        # data_dict[a + 1].append('column' + str(a + 1))
        # data_dict[a + 1].append('attribute' + str(a + 1))
        # data_dict[a + 1].append('feature' + str(a + 1))
        # data_dict[a + 1].append(str(a + 1))
        # data_dict[a + 1].append(att[a])
        # data_dict[a + 1].append(att[a].lower())
        # data_dict[a + 1].append(att[a].replace('_', ' '))
        # data_dict[a + 1].append(att[a].replace(' ', '_'))

        # att_dict[a + 1] = 'column' + str(a + 1)
        # att_dict[a + 1] = 'attribute' + str(a + 1)
        # att_dict[a + 1] = 'feature' + str(a + 1)
        # att_dict[a + 1] = str(a + 1)
        # att_dict[a + 1] = att[a]
        # att_dict[a + 1] = att[a].lower()
        # att_dict[a + 1] = att[a].replace('_', ' ')
        # att_dict[a + 1] = att[a].replace(' ', '_')

    # pprint(att_dict)
    return att_dict


# d = create_indexed_dict()
# pprint(d)
# # print(d[10])
#
# for key in d:
#     print(key)
