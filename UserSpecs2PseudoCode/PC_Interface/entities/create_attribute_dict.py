from pprint import pprint
import read_attributes


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
