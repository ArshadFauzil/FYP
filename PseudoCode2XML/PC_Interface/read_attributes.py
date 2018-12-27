import pandas as pd
import os

# root_path = os.path.normpath(os.getcwd() + os.sep + os.pardir) + '/Resources'
# os.chdir(root_path)


def get_columns(fname):
    df = pd.read_csv(fname, nrows=0, sep='\t', delimiter=None, header='infer', names=None,
                     index_col=None, encoding="ISO-8859-1")

    attributes = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

    # attributes = df.columns.values.tolist()

    # print(len(list(df)))

    for col in attributes:
        attr = col.split(',')

    print(len(attr))
    # print(attr)
    return attr
